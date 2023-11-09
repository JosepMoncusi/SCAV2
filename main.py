import subprocess
import os
import cv2


# TASK 1 - MP4 TO MP2
print('\n TASK 1 - MP4 to MP2')

def mp4_to_mp2(input_file, output_file):
    if os.path.exists(output_file): # Check if the output file already exists
        os.remove(output_file) # Delete it if it exists

    # Run the ffmpeg command to convert the MP4 to MP2
    ffmpeg_command = f'ffmpeg -i {input_file} -c:v mpeg2video -q:v 2 -c:a mp2 {output_file}' # -c:a to specify audio codec
    subprocess.run(ffmpeg_command, shell=True)


def get_video_info(input_file):
    # Run the ffmpeg command to get video information
    ffmpeg_command = f'ffmpeg -i {input_file}'
    result = subprocess.run(ffmpeg_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Parse and save the video information to a text file
    with open(f'{input_file}_info.txt', 'w') as info_file:
        info_file.write(result.stdout)


input_file = 'bunny.mp4'  # Replace with your input MP4 file
output_file = 'BBB.mp2'  # Replace with your output MP2 file

mp4_to_mp2(input_file, output_file)
get_video_info(output_file)

print(f"Conversion and information extraction completed. Output file: {output_file}")

# TASK 2 - MODIFY RESOLUTION
print('\n TASK 2 - Modify resolution')


def modify_resolution(input_file, output_file, width, height):
    # Check if the output file already exists, and delete it if it does
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the ffmpeg command to modify the resolution
    ffmpeg_command = f'ffmpeg -i {input_file} -vf "scale={width}:{height}" {output_file}'
    subprocess.run(ffmpeg_command, shell=True)


output_file_resized = 'BBB_resized.mp4'
modify_resolution(input_file, output_file_resized, width=360, height=360)


# TASK 3 - CHROMA SUBSAMPLING
print('\n TASK 3 - Chroma subsampling')


def change_chroma_subsampling(input_file, output_file, chroma_subsampling):
    # Check if the output file already exists, and delete it if it does
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the ffmpeg command to change chroma subsampling
    ffmpeg_command = f'ffmpeg -i {input_file} -vf "format={chroma_subsampling}" {output_file}'
    subprocess.run(ffmpeg_command, shell=True)


output_file_subsampling = 'BBB_subsampling.mp4'
change_chroma_subsampling(input_file, output_file_subsampling, chroma_subsampling="yuv420p")

print(f"Chroma subsampling modification completed. Output file: {output_file_subsampling}")



#TASK 4 - VIDEO INFO

print('\n TASK 4 - Video info')

def print_video_info(video_path):
    # Create a VideoCapture object and open the video file
    video = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if video.isOpened():
        # Get and print the video properties
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fourcc = video.get(cv2.CAP_PROP_FOURCC)

        print(f"FPS: {fps}")
        print(f"Frame count: {frame_count}")
        print(f"Frame width: {frame_width}")
        print(f"Frame height: {frame_height}")
        print(f"FourCC: {fourcc}")

        # Release the video object
        video.release()
    else:
        # Print an error message if the video file was not opened
        print("Error: Could not open the video file")


print_video_info("bunny.mp4")

#TASK 5 - INHERITANCE

#Since the method didn't work on the previous script, it is now commented so this script don't break.
#Anyway, there is how i have found it should be done

print('\n TASK 5 - Inheritance')


# Importing the resize_and_reduce_quality_ffmpeg function from P1
from rgb_yuv import resize_and_reduce_quality_ffmpeg


video_capture = cv2.VideoCapture(input_file)
success, frame = video_capture.read()

output_resized_reduced = 'BBB_inherited.jpg'
resize_width, resize_height, quality = 640, 480, 20

# Applying the resize_and_reduce_quality_ffmpeg function

#resize_and_reduce_quality_ffmpeg(video_capture, output_resized_reduced, resize_width, resize_height, quality)


