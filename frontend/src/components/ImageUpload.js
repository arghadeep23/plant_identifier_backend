import React, { useState } from 'react';

export function ImageUpload() {
    const [imageUploaded, setImageUploaded] = useState(false);
    const [selectedImage, setSelectedImage] = useState(null);
    const [isLoading, setIsloading] = useState(false);
    let confidence = 0;
    
    const handleImageChange = (event) => {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                setSelectedImage(reader.result);
                setImageUploaded(true);
            };
            reader.readAsDataURL(file);
        } else {
            setSelectedImage(null);
            setImageUploaded(false);
        }
    };

    const handleImageSubmit = () => {
        // Implement your logic for submitting the image here
        // For example, you can send the selectedImage data to your backend or perform further processing.
        // This is a placeholder function and should be replaced with your actual submit logic.
        console.log('Image submitted:', selectedImage);
    };

    return (
        <div className="image-upload">
            <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                className="image-input"
            />
            {!imageUploaded && <p>Enter image file</p>}
            {imageUploaded && (
                <div className="image-preview">
                    <img src={selectedImage} alt="Preview" className="preview-image" />
                    <button onClick={handleImageSubmit}>Submit Image</button>
                </div>
            )}
        </div>
    );
};

// export default ImageUpload; 
