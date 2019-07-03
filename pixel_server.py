from flask import Flask
from flask import Flask, request, send_from_directory
from flask import send_file

from Adafruit_AMG88xx import Adafruit_AMG88xx
from time import sleep

sensor = Adafruit_AMG88xx(busnum=1)

app = Flask(__name__, static_url_path='/static')


def get_pixels():
    raw_data = sensor.readPixels()
    data = []
    for i in range(8):
        #print(raw_data)
        data.append(raw_data[i*8:(i+1)*8])
    return data

@app.route("/img.jpg")
def return_img():
    return send_file('static/cam.jpg')

@app.route("/")
def home():
    data = get_pixels()
    website = "<html>"
    website+="""      
      <script>
         setTimeout(function() {
            location.reload(true);
         }, 250);
      </script>"""
    website += '<body><div style="float:left"><table style="background: url("img.jpg")">'
    for j in range(8):
        website+="<tr>"
        for i in range(8):
            website += '<td><div style="background-color: rgb(%i, 0,0); width:100px; height:100px"><span style="color:grey">%i℃</span></div></td>' % (((data[7-i][7-j] - 15) * (255.0/30)), data[7-i][7-j])
        website+="</tr>"
    website+='</table></div>'
    website+='<div><img src="img.jpg"></div>'
    website+='</body>'
    website+="</html>"

    return(website)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
