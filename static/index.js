labels_dict = { 0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise' }

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
            const result = await response.json();

            // Hiển thị hình ảnh đã xử lý
            const processedImage = result.image;
            document.getElementById('result').innerHTML = `<div class="col-6">
            <img src="data:image/jpeg;base64,${processedImage}">
        </div>`;

            // Hiển thị các kết quả dự đoán
            const resultContainer = document.createElement('div');
            resultContainer.classList.add('col-6');
            result.results.forEach(item => {
                const sortedResults = item.result[0]
                    .map((value, index) => ({ value, index }))
                    .sort((a, b) => b.value - a.value)
                    .slice(0, 3);

                sortedResults.forEach(item => {
                    item.value = (item.value * 100).toFixed(2);
                    let bgClass;
                    if (item.value >= 75) {
                        bgClass = 'bg-success';
                    } else if (item.value >= 50) {
                        bgClass = 'bg-info';
                    } else if (item.value >= 25) {
                        bgClass = 'bg-warning';
                    } else {
                        bgClass = 'bg-danger';
                    }
                    const resultElement = document.createElement('div');
                    resultElement.classList.add('result-item');
                    resultElement.innerHTML = `
                     <div class="card">
              <div class="card-body">
                
                <p class="card-text" style="width: 25%; color: black;"> ${labels_dict[item.index]}</p>
                <div class="progress">
                  <div class="progress-bar ${bgClass}" role="progressbar" style="width: ${item.value}%; color: black;" aria-valuenow="${item.value}" aria-valuemin="0" aria-valuemax="1">${item.value}%</div>
                </div>
              </div>
            </div>
          `;

                    resultContainer.appendChild(resultElement);
                })
            });

            document.getElementById('result').appendChild(resultContainer);
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
    const resultContainer = document.getElementById('resultContainer'); // Container để hiển thị kết quả

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
            const result = await response.json();

            // Hiển thị hình ảnh đã xử lý
            const processedImage = result.image;
            const elements = document.querySelectorAll('.result_realtime_predict');
            elements.forEach(element => {
                element.remove();
            });
            document.getElementById('resultImage').src = `data:image/jpeg;base64,${processedImage}`;
            const resultContainer = document.getElementById('result_realtime');
            const resultContent = document.createElement('div');
            resultContent.classList.add('col-4', 'result_realtime_predict');

            result.results.forEach(item => {
                const sortedResults = item.result[0]
                    .map((value, index) => ({ value, index }))
                    .sort((a, b) => b.value - a.value)
                    .slice(0, 3);
                sortedResults.forEach(item => {
                    item.value = (item.value * 100).toFixed(2);
                    let bgClass;
                    if (item.value >= 75) {
                        bgClass = 'bg-success';
                    } else if (item.value >= 50) {
                        bgClass = 'bg-info';
                    } else if (item.value >= 25) {
                        bgClass = 'bg-warning';
                    } else {
                        bgClass = 'bg-danger';
                    }
                    const resultElement = document.createElement('div');
                    resultElement.classList.add('result-item');
                    resultElement.innerHTML = `
                        <div class="card">
                            <div class="card-body">
    
                                <p class="card-text" style="width: 25%; color: black;"> ${labels_dict[item.index]}</p>
                                <div class="progress">
                                    <div class="progress-bar ${bgClass}" role="progressbar" style="width: ${item.value}%; color: black;" aria-valuenow="${item.value}" aria-valuemin="0" aria-valuemax="1">${item.value}%</div>
                                </div>
                            </div>
                        </div>`;
                    resultContent.appendChild(resultElement);
                })
            })
            resultContainer.appendChild(resultContent);
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

    setTimeout(() => {
        const elements = document.querySelectorAll('.result_realtime_predict');
        elements.forEach(element => {
            element.remove();
        });
    }, 300);
}

document.getElementById('stopCamera').addEventListener('click', stopCamera);
