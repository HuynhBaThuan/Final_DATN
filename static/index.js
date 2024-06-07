// document.getElementById('uploadImage').addEventListener('click', (event) => {
//     event.preventDefault();
//     document.getElementById('imageInput').click();
// });

// document.getElementById('imageInput').addEventListener('change', async (event) => {
//     stopCamera();
//     const file = event.target.files[0];
//     if (file) {
//         const formData = new FormData();
//         formData.append('image', file);

//         const response = await fetch('http://127.0.0.1:5000/detect_faces', {
//             method: 'POST',
//             body: formData,
//         });

//         if (response.ok) {
//             const url = URL.createObjectURL(await response.blob());
//             document.getElementById('result').innerHTML = `<img src="${url}">`;
//         } else {
//             document.getElementById('result').innerHTML = 'Failed to detect faces.';
//         }
//     }
// });

// let videoStream = null;
// let intervalId = null;

// document.getElementById('startCamera').addEventListener('click', async () => {
//     document.getElementById('result').innerHTML = '';
//     const video = document.getElementById('video');
//     const canvas = document.getElementById('canvas');
//     const context = canvas.getContext('2d');

//     try {
//         video.srcObject = await navigator.mediaDevices.getUserMedia({ video: true });
//         videoStream = video.srcObject;
//         // video.style.display = 'none';
//         // canvas.style.display = 'none';
//         document.getElementById('resultImage').style.display = 'block';

//         video.addEventListener('play', () => {
//             intervalId = setInterval(async () => {
//                 if (video.paused || video.ended) {
//                     clearInterval(intervalId);
//                     return;
//                 }

//                 context.drawImage(video, 0, 0, canvas.width, canvas.height);
//                 const imageData = canvas.toDataURL('image/jpeg');

//                 const response = await fetch('http://127.0.0.1:5000/detect_faces_realtime', {
//                     method: 'POST',
//                     body: JSON.stringify({ image: imageData }),
//                     headers: { 'Content-Type': 'application/json' },
//                 });

//                 if (response.ok) {
//                     const url = URL.createObjectURL(await response.blob());
//                     document.getElementById('resultImage').src = url;
//                 }
//             }, 200);
//         });
//     } catch (error) {
//         console.error('Error accessing camera:', error);
//     }
// });

// function stopCamera () {
//     if (videoStream) {
//         videoStream.getTracks().forEach(track => track.stop());
//         document.getElementById('video').srcObject = null;
//         videoStream = null;
//     }
//     if (intervalId) {
//         clearInterval(intervalId);
//         intervalId = null;
//     }
//     document.getElementById('resultImage').style.display = 'none';
// }

// document.getElementById('stopCamera').addEventListener('click', stopCamera);

document.getElementById('uploadImage').addEventListener('click', (event) => {
    event.preventDefault();
    document.getElementById('imageInput').click();
});

document.getElementById('imageInput').addEventListener('change', async (event) => {
    stopCamera();
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        const response = await fetch('http://127.0.0.1:5000/detect_faces', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const url = URL.createObjectURL(await response.blob());
            document.getElementById('result').innerHTML = `<img src="${url}">`;
        } else {
            document.getElementById('result').innerHTML = 'Failed to detect faces.';
        }
    }
});

let videoStream = null;
let intervalId = null;

document.getElementById('startCamera').addEventListener('click', async () => {
    stopCamera(); // Ensure any existing streams and intervals are stopped
    document.getElementById('result').innerHTML = '';
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    try {
        video.srcObject = await navigator.mediaDevices.getUserMedia({ video: true });
        videoStream = video.srcObject;
        document.getElementById('resultImage').style.display = 'block';

        video.addEventListener('play', handlePlayEvent, { once: true });
    } catch (error) {
        console.error('Error accessing camera:', error);
    }
});

async function handlePlayEvent() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    intervalId = setInterval(async () => {
        if (video.paused || video.ended) {
            clearInterval(intervalId);
            return;
        }

        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');

        const response = await fetch('http://127.0.0.1:5000/detect_faces_realtime', {
            method: 'POST',
            body: JSON.stringify({ image: imageData }),
            headers: { 'Content-Type': 'application/json' },
        });

        if (response.ok) {
            const url = URL.createObjectURL(await response.blob());
            document.getElementById('resultImage').src = url;
        }
    }, 200);
}

function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        document.getElementById('video').srcObject = null;
        videoStream = null;
    }
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    document.getElementById('resultImage').style.display = 'none';
}

document.getElementById('stopCamera').addEventListener('click', stopCamera);
