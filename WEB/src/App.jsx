import React, {useRef, useState} from "react";
import axios from "axios";
import "./App.css";


const App = () => {
    const [image, setImage] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [drawing, setDrawing] = useState(false);
    const canvasRef = useRef(null);
    const [probabilities, setProbabilities] = useState(null);

    const startDrawing = (e) => {
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
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
        const scaledCanvas = document.createElement("canvas");
        const scaledContext = scaledCanvas.getContext("2d");

        scaledCanvas.width = 280;
        scaledCanvas.height = 280;

        scaledContext.drawImage(canvas, 0, 0, 280, 280);

        const imageData = scaledContext.getImageData(0, 0, 280, 280);
        const tempCanvas = document.createElement("canvas");

        tempCanvas.width = 280;
        tempCanvas.height = 280;

        const tempContext = tempCanvas.getContext("2d");
        tempContext.putImageData(imageData, 0, 0);
        const imageDataURL = tempCanvas.toDataURL("image/jpeg");
        setImage(imageDataURL);
    };

    const resetCanvas = () => {
        setPrediction(null);
        setProbabilities(null);
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
        context.clearRect(0, 0, canvas.width, canvas.height);
    };

    const handleSubmit = () => {
        endDrawing();
        axios
            .post(`${import.meta.env.VITE_BACKEND_URL}/api/interrogate`, {image})
            .then((response) => {
                setPrediction(response.data.predictedClasses);
                setProbabilities(response.data.predictedProbability);
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
                <div id="canvas-div" style={{marginTop:"30px"}}>
                    <canvas
                        ref={canvasRef}
                        id="canvas"
                        width="280"
                        height="280"
                        style={{backgroundColor: "black"}}
                        onMouseDown={startDrawing}
                        onMouseMove={draw}
                        onMouseUp={endDrawing}
                    />
                </div>
                <div style={{display:'flex', alignItems:'center', marginTop:'30px'}}>
                    <button style={{marginRight:"20px"}} onClick={handleSubmit}>Predict</button>
                    <button onClick={resetCanvas}>Reset Canvas</button>
                </div>
                <div style={{display:'flex', alignItems:'center', marginTop:'30px'}}>
                    <h3 style={{color : 'white'}}>Prediction : </h3>
                    <h2 style={{color : 'white', marginLeft:3}}>{prediction}</h2>
                </div>
                <h3 style={{color : 'white'}}>Précision : {probabilities ?`${probabilities.toFixed(2)} %` : ''} </h3>
            </section>
        </div>
    );
};

export default App;
