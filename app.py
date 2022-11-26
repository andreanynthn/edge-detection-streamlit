import cv2
import av
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, ClientSettings, VideoProcessorBase

def main():
    st.title("Edge Detection OpenCv")
    st.write("Created by: Andrean Yonathan")

    source = st.radio("Select source:", ("Camera", "File"))

    if source == "File":
        image = st.file_uploader("Upload image", type = ['jpg', 'png', 'jpeg'])
        lower = st.slider("Lower threshold", min_value = 0, max_value = 1000, step = 1, value = 100)
        upper = st.slider("Uppder threshold", min_value = 0, max_value = 1000, step = 1, value = 200)

        if image is not None:
            img = Image.open(image)

            if st.button("Process"):
                # convert to numpy array
                img = np.array(img)

                canny_image = cv2.Canny(img, lower, upper)
                st.image(canny_image)

    if source == "Camera":
        lower = st.slider("Lower threshold", min_value = 0, max_value = 1000, step = 1, value = 100)
        upper = st.slider("Uppder threshold", min_value = 0, max_value = 1000, step = 1, value = 100)

        def callback(frame):
            img = frame.to_ndarray(format = "bgr24")
            img = cv2.Canny(img, lower, upper)
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        ctx = webrtc_streamer(
            key="edge-detection",
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": False},
            video_frame_callback=callback
        )

if __name__ == '__main__':
    main()