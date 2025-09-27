import React, { useState, useRef, useCallback } from 'react';
import { Box, Typography, Button, Container, Paper, Grid, CircularProgress, Tabs, Tab } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import './CropDoctorPage.css'; // Ensure this CSS file is created and styled

// ResultCard component to handle the 3D flip animation
const ResultCard = ({ data, result, onFetchPrecautions, index }) => {
    // The 'is-flipped' class will be added when a diagnosis is available
    const isDiagnosed = result && (result.disease || result.error);

    return (
        <div className={`flip-card ${isDiagnosed ? 'is-flipped' : ''}`}>
            <div className="flip-card-inner">
                {/* Front of the card: The Uploaded Image */}
                <div className="flip-card-front">
                    {data.file.type.startsWith('video/') ? (
                        <video src={data.preview} className="preview-media" controls />
                    ) : (
                        <img src={data.preview} alt={`preview ${index}`} className="preview-media" />
                    )}
                </div>

                {/* Back of the card: The Diagnosis Result */}
                <div className="flip-card-back">
                    {result?.error ? (
                        <div className="result-content">
                            <Typography color="error" variant="h6">Error</Typography>
                            <Typography color="error">{result.error}</Typography>
                        </div>
                    ) : (
                        <div className="result-content">
                            <Typography variant="h6" gutterBottom>Diagnosis Result</Typography>
                            <Typography><b>Disease:</b> {result?.disease}</Typography>
                            <Typography><b>Confidence:</b> {result?.confidence}</Typography>

                            {result?.precautions ? (
                                result.precautions.error ? (
                                    <Typography color="error">{result.precautions.error}</Typography>
                                ) : (
                                    <div className="precautions-section">
                                        <Typography variant="subtitle1"><b>{result.precautions.disease_name}</b></Typography>
                                        <p><b>Symptoms:</b> {result.precautions.symptoms_summary}</p>
                                        
                                        <p><b>Prevention:</b></p>
                                        <ul>{result.precautions.prevention?.map((tip, i) => <li key={i}>{tip}</li>)}</ul>
                                        
                                        <p><b>Organic Treatment:</b></p>
                                        <ul>{result.precautions.treatment?.organic_methods?.map((method, i) => <li key={i}>{method}</li>)}</ul>

                                        <p><b>Chemical Treatment:</b></p>
                                        <ul>{result.precautions.treatment?.chemical_methods?.map((method, i) => <li key={i}>{method}</li>)}</ul>
                                    </div>
                                )
                            ) : (
                                result?.disease && result.disease.toLowerCase() !== 'healthy' && (
                                    <Box sx={{ mt: 2, textAlign: 'center' }}>
                                        {result?.precautionsLoading ? (
                                            <CircularProgress size={24} />
                                        ) : (
                                            <Button
                                                variant="contained"
                                                onClick={() => onFetchPrecautions(index, result.disease)}
                                            >
                                                Get Precautions
                                            </Button>
                                        )}
                                    </Box>
                                )
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

// Main CropDoctorPage component
const CropDoctorPage = () => {
    const navigate = useNavigate();
    const [filesData, setFilesData] = useState([]);
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [tabIndex, setTabIndex] = useState(0);
    const webcamRef = useRef(null);

    const handleFileChange = (e) => {
        if (e.target.files) {
            const filesArray = Array.from(e.target.files).map(file => ({
                file: file,
                preview: URL.createObjectURL(file)
            }));
            setFilesData(filesArray);
            setResults(new Array(filesArray.length).fill({}));
        }
    };

    const capturePhoto = useCallback(() => {
        console.log("Attempting to capture photo. Webcam ref:", webcamRef.current);
        if (webcamRef.current) {
            const imageSrc = webcamRef.current.getScreenshot();
            if (imageSrc) {
                fetch(imageSrc)
                    .then(res => res.blob())
                    .then(blob => {
                        const file = new File([blob], `capture-${Date.now()}.jpeg`, { type: 'image/jpeg' });
                        setFilesData(prev => [...prev, { file, preview: imageSrc }]);
                        setResults(prev => [...prev, {}]);
                        console.log("Photo captured and added to state.");
                    });
            } else {
                 console.error("getScreenshot() returned null. Is the camera active?");
            }
        } else {
            console.error("Webcam ref is not set. Cannot capture photo.");
        }
    }, [webcamRef]);

    const handleDiagnose = async () => {
        setLoading(true);
        const diagnosisPromises = filesData.map(async (data) => {
            if (!data.file.type.startsWith('image/')) {
                return { error: 'Diagnosis is only supported for images.' };
            }
            
            const formData = new FormData();
            formData.append('file', data.file);

            try {
                const res = await fetch('http://127.0.0.1:5000/diagnose', { method: 'POST', body: formData });
                const text = await res.text();
                if (!res.ok) throw new Error(`Server Error: ${text}`);
                return JSON.parse(text);
            } catch (error) {
                return { error: `Failed to diagnose. ${error.message}` };
            }
        });

        const newResults = await Promise.all(diagnosisPromises);
        setResults(newResults);
        setLoading(false);
    };

    const handleFetchPrecautions = async (index, disease) => {
        setResults(prevResults =>
            prevResults.map((result, i) =>
                i === index ? { ...result, precautionsLoading: true } : result
            )
        );

        try {
            const res = await fetch('http://127.0.0.1:5000/precautions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ disease }),
            });

            if (!res.ok) {
                throw new Error('Server responded with an error.');
            }
            const data = await res.json();

            setResults(prevResults =>
                prevResults.map((result, i) =>
                    i === index
                        ? { ...result, precautions: data, precautionsLoading: false }
                        : result
                )
            );
        } catch (error) {
            setResults(prevResults =>
                prevResults.map((result, i) =>
                    i === index
                        ? { ...result, precautions: { error: error.message }, precautionsLoading: false }
                        : result
                )
            );
        }
    };

    return (
        <div className="crop-doctor-container">
            <header className="crop-doctor-header">
                <Typography variant="h4" component="h1">Crop Doctor</Typography>
                <Button variant="outlined" onClick={() => navigate('/')}>Back to Home</Button>
            </header>

            <Container maxWidth="lg" className="crop-doctor-main">
                <Paper elevation={3} sx={{ borderRadius: '12px', overflow: 'hidden', mb: 4 }}>
                    <Tabs value={tabIndex} onChange={(e, newValue) => setTabIndex(newValue)} centered>
                        <Tab label="Upload Files" />
                        <Tab label="Use Live Camera" />
                    </Tabs>
                    {tabIndex === 0 && (
                        <div className="upload-section">
                            <Typography variant="h5" gutterBottom>Upload Crop Images</Typography>
                            <Button variant="contained" component="label">
                                Select Files
                                <input type="file" hidden multiple accept="image/*,video/*" onChange={handleFileChange} />
                            </Button>
                        </div>
                    )}
                    {tabIndex === 1 && (
                        <div className="camera-section">
                            <Webcam
                                audio={false}
                                ref={webcamRef}
                                screenshotFormat="image/jpeg"
                                className="webcam-feed"
                            />
                            <Button variant="contained" onClick={capturePhoto}>Capture Photo</Button>
                        </div>
                    )}
                </Paper>

                {filesData.length > 0 && (
                    <>
                        <Typography variant="h5" sx={{ mt: 4, mb: 3, textAlign: 'center' }}>Your Uploads</Typography>
                        <Grid container spacing={5} justifyContent="center">
                            {filesData.map((data, index) => (
                                <Grid item key={index} xs={11} sm={8} md={5} lg={4}>
                                    <ResultCard 
                                        data={data}
                                        result={results[index]}
                                        onFetchPrecautions={handleFetchPrecautions}
                                        index={index}
                                    />
                                </Grid>
                            ))}
                        </Grid>

                        <Box sx={{ textAlign: 'center', mt: 4, mb: 3 }}>
                            <Button variant="contained" size="large" onClick={handleDiagnose} disabled={loading}>
                                {loading ? <CircularProgress size={24} color="inherit" /> : 'Diagnose All'}
                            </Button>
                        </Box>
                    </>
                )}
            </Container>
        </div>
    );
};

export default CropDoctorPage;
