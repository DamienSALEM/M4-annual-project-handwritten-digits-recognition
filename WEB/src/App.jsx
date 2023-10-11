import React, { useState, useRef } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [drawing, setDrawing] = useState(false);

  const canvasRef = useRef(null);

  const startDrawing = (e) => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.fillStyle = "white";
    context.strokeStyle = "white";
    context.lineWidth = 10; 
    context.beginPath();
    context.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    setDrawing(true);
  };

  const draw = (e) => {
    if (!drawing) return;
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    context.stroke();
  };

  const endDrawing = () => {
    setDrawing(false);
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    const scaledCanvas = document.createElement("canvas");
    const scaledContext = scaledCanvas.getContext("2d");

    scaledCanvas.width = 28;
    scaledCanvas.height = 28;

    scaledContext.drawImage(canvas, 0, 0, 28, 28);

    const imageDataURL = scaledCanvas.toDataURL("image/png");
    
    setImage(imageDataURL);
  };

  const resetCanvas = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
  };

  const handleSubmit = () => {
    endDrawing();
    console.log(image);
    axios
      .post("http://localhost:8000/api/interrogate", { image })
      .then((response) => {
        setPrediction(response.data.prediction);
        setImageResult(response.data.image);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div>
        <section className="nav">
            <h1>DIGIT RECOGNIZER</h1>
            <h3 className="span loader">
                <span className="m">H</span>
                <span className="m">A</span>
                <span className="m">N</span>
                <span className="m">D</span>
                <span className="m">W</span>
                <span className="m">R</span>
                <span className="m">I</span>
                <span className="m">T</span>
                <span className="m">T</span>
                <span className="m">E</span>
                <span className="m">N</span>
                <span className="m">&nbsp;</span>
                <span className="m">D</span>
                <span className="m">I</span>
                <span className="m">G</span>
                <span className="m">I</span>
                <span className="m">T</span>
                <span className="m">S</span>
                <span className="m">&nbsp;</span>
                <span className="m">R</span>
                <span className="m">E</span>
                <span className="m">C</span>
                <span className="m">O</span>
                <span className="m">G</span>
                <span className="m">N</span>
                <span className="m">I</span>
                <span className="m">T</span>
                <span className="m">I</span>
                <span className="m">O</span>
                <span className="m">N</span>
            </h3>
          <div id="canvas-div">
            <canvas
              ref={canvasRef}
              id="canvas"
              width="280"
              height="280"
              style={{ backgroundColor: "black" }}
              onMouseDown={startDrawing}
              onMouseMove={draw}
              onMouseUp={endDrawing}
              onMouseOut={endDrawing}
            />
          </div>
          <div><button onClick={handleSubmit}>Predict</button> <button onClick={resetCanvas}>Reset Canvas</button> </div>
          <p>Prediction: {prediction}</p>
          
        </section>
    </div>
  );
};

export default App;
