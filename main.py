from  tkinter import *
import tkinter.messagebox as msgb
from tkinter import filedialog

import os

from PIL import Image, ImageDraw, ImageFont,ImageTk

root = Tk()
root.title('Image Watermarking')
root.geometry("500x820")

frame = Frame(root)


def on_validate(new_text):
    # Check if the length of the new text exceeds the limit (10 characters)
    if len(new_text) > 30:
        return False
    return True

validate_command = root.register(on_validate)
    
def create_directory_if_not_exists(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # If it doesn't exist, create it
        os.makedirs(directory_path)


def select_main_pct():
    global img, img_display
    filename = filedialog.askopenfilename(initialdir='/Downloads', title='Select image', filetypes=(('png images', '*.png'), ('jpg images', '*.jpg')))
    img = Image.open(filename)

    # Resize the original image and display it on the label
    img_display = img.resize((400, 350), Image.ANTIALIAS)
    img_display = ImageTk.PhotoImage(img_display)
    lbl_show_picture['image'] = img_display

    logo_option_btn.pack(pady=5)
    or_label.pack()
    text_option_btn.pack()

    # Automatically save the original image to a specified location
    save_directory = 'uploaded_image'  # Replace this with the desired directory path
    create_directory_if_not_exists(save_directory)
    img_path = os.path.join(save_directory, 'original_image.jpg')  # You can change the filename and extension as needed
    img.save(img_path)


logo_selected = False
def select_logo_pct():
    global logo_img, logo_img_display, logo_selected
    filename = filedialog.askopenfilename(initialdir='/Downloads',title='Select image', filetypes=(('png images','*.png'),('jpg images','*.jpg')))
    if filename:
        logo_img = Image.open(filename)

        logo_img_display = logo_img.resize((100,100),Image.ANTIALIAS)
        logo_img_display = ImageTk.PhotoImage(logo_img_display)
        lbl_show_logo['image'] = logo_img_display

        # Automatically save the original image to a specified location
        save_directory = "uploaded_logo" 
        create_directory_if_not_exists(save_directory) # Replace this with the desired directory path
        img_path = os.path.join(save_directory, 'logo_image.jpg')  # You can change the filename and extension as needed
        logo_img.save(img_path)
        logo_selected = True


def close_the_app():
    if msgb.askokcancel("Quit", "Do you want to close the app? Make sure that you downloaded the Watermarked Image"):
        root.destroy()

def text_watermark_options():
    watermark_text_label.pack()
    watermark_text_entry.pack()
    watermark_text_entry.focus_set()

    place_label.pack()
    place_option_menu.pack()

    color_label.pack()
    color_option_menu.pack()

    text_size_label.pack()
    text_size_option_menu.pack()

    logo_option_btn.config(text='Confirm',bg='#00cc66', command=add_text_watermark)
    text_option_btn.config(text='Close The App',bg='#e30022',fg='white', command=close_the_app)


def logo_watermark_options():
    place_label.pack()
    place_option_menu.pack()

    logo_size_label.pack()
    logo_size_option_menu.pack()

    logo_upload_btn.pack()
    lbl_show_logo.pack(pady=5)

    logo_option_btn.config(text='Confirm',bg='#00cc66',command=add_logo_watermark)
    text_option_btn.config(text='Close The App',bg='#e30022',fg='white',command=close_the_app)


def add_text_watermark():
    position = place_selected_option_var.get()
    font_size = int(text_size_selected_option_var.get())
    color = color_selected_option_var.get().lower()

    if watermark_text_entry.get() == '':
        msgb.showerror("Error", "Please add text before confirming.")
        return
    
    img = Image.open("uploaded_image/original_image.jpg")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    font = ImageFont.truetype("arial.ttf", font_size)
    
    text_width, text_height = draw.textsize(watermark_text_entry.get(), font=font)
 
    if position == "Top Left":
        x, y = 10, 10
    elif position == "Top Right":
        x, y = width - text_width - 10, 10
    elif position == "Bottom Left":
        x, y = 10, height - text_height - 10
    elif position == "Bottom Right":
        x, y = width - text_width - 10, height - text_height - 10
    else:
        x, y = (width - text_width) // 2, (height - text_height) // 2
    
    draw.text((x, y), watermark_text_entry.get(), font=font, fill=color)
    create_directory_if_not_exists('watermarked_image')
    img.save("watermarked_image/image_with_watermark.jpg")
    # watermark_text_entry.delete(0, END)
    show_watermarked_image()
    

def add_logo_watermark():
    position = place_selected_option_var.get()
    logo_size = tuple(map(int,logo_size_selected_option_var.get().strip("()").split(", ")))

    if not logo_selected:
        msgb.showerror("Error", "Please select the logo before confirming.")
        return

    img = Image.open("uploaded_image/original_image.jpg")
    logo = Image.open("uploaded_logo/logo_image.jpg").convert("L")  # Convert to 8-bit grayscale
    logo = logo.resize(logo_size, Image.LANCZOS)  # Use Image.LANCZOS for resampling
    
    width, height = img.size
    logo_width, logo_height = logo.size
    
    if position == "Top Left":
        x, y = 10, 10
    elif position == "Top Right":
        x, y = width - logo_width - 10, 10
    elif position == "Bottom Left":
        x, y = 10, height - logo_height - 10
    elif position == "Bottom Right":
        x, y = width - logo_width - 10, height - logo_height - 10
    else:
        x, y = (width - logo_width) // 2, (height - logo_height) // 2
    
    img.paste(logo, (x, y), logo)  # Use the logo image as the transparency mask
    create_directory_if_not_exists('watermarked_image')
    img.save("watermarked_image/image_with_watermark.jpg")
    show_watermarked_image()


def show_watermarked_image():
    # Display the watermarked image on the screen
    msgb.showinfo('Your Watermark Successfully was added on the Image. You Can now see that on the screen and download it')
    watermarked_img = Image.open("watermarked_image/image_with_watermark.jpg")
    watermarked_img = watermarked_img.resize((400, 350), Image.ANTIALIAS)
    watermarked_img = ImageTk.PhotoImage(watermarked_img)
    lbl_show_picture['image'] = watermarked_img

    # Update the global variable img_display to use it later in other functions
    global img_display
    img_display = watermarked_img
    download_button.pack()


def download_image():
    # Get the path to the image file you want to download
    image_path = "watermarked_image/image_with_watermark.jpg"  # Replace this with the actual path to your image file

    # Ask the user to choose the download location and filename
    download_path = filedialog.asksaveasfilename(initialdir="/", title="Save Image As", defaultextension=".jpg", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))

    # If the user canceled the download or didn't choose a location, return without doing anything
    if not download_path:
        return

    # Check if the chosen file already exists, and if it does, ask the user for confirmation to overwrite it
    if os.path.exists(download_path):
        if not msgb.askokcancel("Warning", "File already exists. Do you want to overwrite it?"):
            return

    # Copy the image file to the chosen download location
    try:
        with open(image_path, "rb") as source_file:
            with open(download_path, "wb") as destination_file:
                destination_file.write(source_file.read())
        msgb.showinfo("Success", "Image downloaded successfully!")
    except Exception as e:
        msgb.showerror("Error", f"Failed to download image: {e}")

lbl_show_picture = Label(frame)
upload_btn = Button(frame,text='Select Image', bg='#FFCC33' ,font=('verdana',16),padx=10,pady=5)

logo_option_btn = Button(text='Add Logo Watermark', bg='#0067cc',fg='white',font=('verdana',16),command=logo_watermark_options)
or_label = Label(text='OR')
text_option_btn = Button(text='Add Text Watermark', bg='#0067cc' ,fg='white',font=('verdana',16),command=text_watermark_options)

# Create the OptionMenu widgets
place_options = ["Top Right", "Top Left", "Bottom Right", "Bottom Left", "Middle"]
text_color_options = ['White',"Black","Purple","Red", "Green", "Yellow", "Blue", "Lightblue",'Orange',"Pink", "Brown", "Gray","Silver"]
text_size_options = [30,50,70,90,110,130,150]
logo_size_options = [(50, 50),(70, 70),(90, 90),(110, 110),(130, 130),(150, 150)]

# Variable to store the selected options
place_selected_option_var = StringVar(root)
color_selected_option_var = StringVar(root)
text_size_selected_option_var = StringVar(root)
logo_size_selected_option_var = StringVar(root)

# Set the default options
place_selected_option_var.set(place_options[0])  
color_selected_option_var.set(text_color_options[0])
text_size_selected_option_var.set(text_size_options[3])
logo_size_selected_option_var.set(logo_size_options[3])

place_option_menu = OptionMenu(root, place_selected_option_var, *place_options)
color_option_menu = OptionMenu(root, color_selected_option_var, *text_color_options)
text_size_option_menu = OptionMenu(root, text_size_selected_option_var, *text_size_options)
logo_size_option_menu = OptionMenu(root, logo_size_selected_option_var, *logo_size_options)

place_label = Label(text='Add Place for Watermark')
color_label = Label(text='Choose Color for Text')
text_size_label = Label(text='Choose Size for Text')
logo_size_label = Label(text='Choose Size for Logo')

watermark_text_label = Label(text='Watermark Text(max 30 symbols)')
watermark_text_entry = Entry(root, validate="key", validatecommand=(validate_command, '%P'))

logo_upload_btn = Button(text='Select Logo')
lbl_show_logo = Label()

frame.pack()
upload_btn.pack(pady=10)
lbl_show_picture.pack()

upload_btn['command'] = select_main_pct
logo_upload_btn['command'] = select_logo_pct

download_button = Button(root,text='Download',bg='green',command=download_image)

root.mainloop()