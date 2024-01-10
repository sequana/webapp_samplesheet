import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
from PIL import Image 


def main():
    st.title("Sample Sheet validator")

    menu = ["Sample Sheet Validation (Illumina)","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")
        image_file = st.file_uploader("Upload Image",type=['png','jpeg','jpg'])
        if image_file is not None:
            # To See Details
            # st.write(type(image_file))
            # st.write(dir(image_file))
            file_details = {"Filename":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
            st.write(file_details)

            img = load_image(image_file)
            st.image(img,width=250)


    elif choice == "Sample Sheet Validation (Illumina)":
        st.subheader("Sample Sheet Validation (Illumina)")
        data_file = st.file_uploader("Upload CSV",type=['csv'])
        if st.button("Process"):
            if data_file is not None:
                file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
                st.write(file_details)

                from sequana.iem import IEM
                iem = IEM(data_file.name)
                try:
                    st.write(f"This sample sheet contains {len(iem.df)} samples")
                    iem.validate()
                except SystemExit as err:
                    st.write(err)
                else:
                    st.write("OK")
    else:
        st.subheader("About")
        st.info("Built with Streamlit")
        st.info("Thomas Cokelaer")
        st.text("Institut Pasteur, Paris, France")



if __name__ == '__main__':
    main()
