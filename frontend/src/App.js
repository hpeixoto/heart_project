import React, { useState } from "react";
import { Container, Typography, TextField, Button, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions } from "@mui/material";

const chestPainTypes = ["typical angina", "atypical angina", "non-anginal", "asymptomatic"];
const restecgTypes = ["normal", "lv hypertrophy"];
const thalTypes = ["normal", "fixed defect", "reversable defect"];

function App() {
    const [formData, setFormData] = useState({
        age: "",
        sex: "",
        cp: "",
        trestbps: "",
        chol: "",
        fbs: "",
        restecg: "",
        thalch: "",
        exang: "",
        oldpeak: ""
    });
    const [result, setResult] = useState("");
    const [recall, setRecall] = useState("");
    const [open, setOpen] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value || "" });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formDataFormatted = new URLSearchParams(formData);

        const response = await fetch("http://127.0.0.1:5000/predict", {  // Use 127.0.0.1 instead of "localhost"
          method: "POST",
          body: new URLSearchParams(formData),
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });

        const data = await response.json();
        setResult(data.prediction);
        setRecall(data.recall ? (data.recall * 100).toFixed(2) : "N/A"); // Convert recall to percentage
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    return (
        <Container maxWidth="sm" style={{ marginTop: "20px" }}>
            <Typography variant="h4" gutterBottom>
                Heart Failure Prediction
            </Typography>
            <form onSubmit={handleSubmit}>
                <TextField label="Age" name="age" type="number" fullWidth margin="normal" onChange={handleChange} value={formData.age} />
                <TextField select label="Sex" name="sex" fullWidth margin="normal" onChange={handleChange} value={formData.sex}>
                    <MenuItem value="">Select</MenuItem>
                    <MenuItem value="Male">Male</MenuItem>
                    <MenuItem value="Female">Female</MenuItem>
                </TextField>
                <TextField select label="Chest Pain Type" name="cp" fullWidth margin="normal" onChange={handleChange} value={formData.cp}>
                    <MenuItem value="">Select</MenuItem>
                    {chestPainTypes.map((type) => (
                        <MenuItem key={type} value={type}>{type}</MenuItem>
                    ))}
                </TextField>
                <TextField label="Resting Blood Pressure" name="trestbps" type="number" fullWidth margin="normal" onChange={handleChange} value={formData.trestbps} />
                <TextField label="Serum Cholesterol" name="chol" type="number" fullWidth margin="normal" onChange={handleChange} value={formData.chol} />
                <TextField select label="Fasting Blood Sugar" name="fbs" fullWidth margin="normal" onChange={handleChange} value={formData.fbs}>
                    <MenuItem value="">Select</MenuItem>
                    <MenuItem value="True">True</MenuItem>
                    <MenuItem value="False">False</MenuItem>
                </TextField>
                <TextField select label="Rest ECG" name="restecg" fullWidth margin="normal" onChange={handleChange} value={formData.restecg}>
                    <MenuItem value="">Select</MenuItem>
                    {restecgTypes.map((type) => (
                        <MenuItem key={type} value={type}>{type}</MenuItem>
                    ))}
                </TextField>
                <TextField label="Maximum Heart Rate" name="thalch" type="number" fullWidth margin="normal" onChange={handleChange} value={formData.thalch} />
                <TextField select label="Exercise Induced Angina" name="exang" fullWidth margin="normal" onChange={handleChange} value={formData.exang}>
                    <MenuItem value="">Select</MenuItem>
                    <MenuItem value="True">True</MenuItem>
                    <MenuItem value="False">False</MenuItem>
                </TextField>
                <TextField label="Oldpeak" name="oldpeak" type="number" fullWidth margin="normal" onChange={handleChange} value={formData.oldpeak} />               
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Predict
                </Button>
                
            </form>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle style={{ color: result === "At Risk" ? "red" : "green" }}>
                    {result === "At Risk" ? "Warning: High Risk" : "Good News: Low Risk"}
                </DialogTitle>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">Close</Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
}

export default App;