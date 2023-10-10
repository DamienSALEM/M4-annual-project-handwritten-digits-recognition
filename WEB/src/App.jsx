import React, { useState, useRef } from "react";
import axios from "axios";

const App = () => {
  const [image, setImage] = useState(null);
  const [imageResult, setImageResult] = useState(null);
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
      <h1>Handwritten Digit Recognition Web App</h1>
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
        <img src={imageResult} alt="result" />
      </div>
      <button onClick={handleSubmit}>Predict</button>
      <button onClick={resetCanvas}>Reset Canvas</button> 
      <p>Prediction: {prediction}</p>
    </div>
  );
};

export default App;
