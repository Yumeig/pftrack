import pfpy
from pfpy import Tracker, Clip
import os

def pfNodeName():
    return 'Export_TrackPosition'

def pfNodeTopLevelButton():
    return 1

def pfAutoRun():
    return False


def main():
    """export TrackPosition for After Effects (.ma)"""
    num = pfpy.getNumTrackers()

    c = pfpy.getClipRef(0)
    width =  c.getFrameWidth()
    height =  c.getFrameHeight()
    asp = float(c.getPixelAspect())
    inPoint = c.getInPoint()
    outPoint = c.getOutPoint()

    x = '//Maya ASCII 4.0 scene\n\n\
    requires maya "4.0";\n\
    currentUnit -l cm -a deg -t pal;\n\
    createNode camera -n "Camera\n\n\
    createNode transform -n "CameraGroup_1";\n\n'

    for i in range(num):
        t = pfpy.getTrackerRef(i)
        name = t.getName()
        x += 'createNode transform -n "{0}";\n'.format(name)
        x += 'createNode locator -n "Null_{0}" -p "{0}";\n'.format(name)

        x += 'createNode animCurveTL -n "{0}_tX";\n'.format(name)
        x += '\tsetAttr -s {0} ".ktv[{1}:{2}]" '.format(outPoint, 0, outPoint-1)
        for j in range(inPoint,outPoint+1):
            x += '{0} {1} '.format(j-1, t.getTrackPosition(j)[0])
        x += ';'

        x += '\ncreateNode animCurveTL -n "{0}_tY";\n'.format(name)
        x += '\tsetAttr -s {0} ".ktv[{1}:{2}]" '.format(outPoint, 0, outPoint-1)
        for j in range(inPoint,outPoint+1):
            x += '{0} {1} '.format(j-1, (height - t.getTrackPosition(j)[1]) * -1)
        x += ';'

        x += '\nconnectAttr "{0}_tX.o" "{0}.tx";'.format(name)
        x += '\nconnectAttr "{0}_tY.o" "{0}.ty";\n\n'.format(name)

    x += '\nselect -ne :defaultResolution;\n'
    x += '\tsetAttr ".w" '+'%d'%width+';\n'
    x += '\tsetAttr ".h" '+'%d'%height+';\n'
    x += '\tsetAttr ".pa" '+'%f'%asp+';\n'
    x += '\tsetAttr ".al" yes;\n'
    x += '\tsetAttr ".dar" '+'%g'%(float(width)*asp/float(height))+';\n'

    with open(os.path.expanduser('~/Desktop/TrackerPosition.ma'), 'w') as f:
        f.write(x)


if __name__ == '__main__':
    main()
