import subprocess as sp
import cv2 as cv

# -------------------------------------------------------------------------------------
video_path = "path_to_your_local_video.mp4"  
rtmpUrl = "path_yo_your_rtmp"
cap = cv.VideoCapture(video_path)

# Get video information
fps = int(cap.get(cv.CAP_PROP_FPS))
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

print(width, height)
# ffmpeg command
command = ['ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "{}x{}".format(width, height),
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-f', 'flv', 
        rtmpUrl]

# 管道配置
p = sp.Popen(command, stdin=sp.PIPE)
# size = (width, height)
# result = cv.VideoWriter("File.avi",cv.VideoWriter_fourcc(*'MJPG'), 10, size)

# read webcamera
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        print("Opening camera is failed")
        break
    #else:
        #result.write(frame)
        #if cv.waitKey(1) & 0xFF == ord('s'):
            #break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    p.stdin.write(frame.tostring())
cap.release()
#result.release()
cv.destroyAllWindows()
p.stdin.flush()
p.stdin.close()
# p.stdout.close()
p.wait()
print("Success")

