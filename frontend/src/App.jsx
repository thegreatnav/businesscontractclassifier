import React, { useState } from 'react';
import './App.css';

function App() {
  const [templateFile, setTemplateFile] = useState(null);
  const [exampleFile, setExampleFile] = useState(null);
  const [backendData, setBackendData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTemplateFileChange = (e) => {
    setTemplateFile(e.target.files[0]);
  };

  const handleExampleFileChange = (e) => {
    setExampleFile(e.target.files[0]);
  };

  // const handleSubmit = async () => {
  //   setLoading(true);
  //   const formData = new FormData();
  //   formData.append('template', templateFile);
  //   formData.append('example', exampleFile);

  //   try {
  //     const response = await fetch('http://127.0.0.1:5001/process', {
  //       method: 'POST',
  //       body: formData
  //     });
  //     if (!response.ok) {
  //       throw new Error('Network response was not ok');
  //     }
  //     const data = await response.json();
  //     setBackendData(data.report); // Accessing the report property from the backend response
  //   } catch (error) {
  //     console.error('There was a problem with the fetch operation:', error);
  //   } finally {
  //     setLoading(false);
  //   }
  // };
  const handleSubmit = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('template', templateFile);
    formData.append('example', exampleFile);

    try {
      const response = await fetch('/process', {
        method: 'POST',
        body: formData
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setBackendData(data.report);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    } finally {
      setLoading(false);
    }
  };

  // const handleSubmit = async () => {
  //   const formData = new FormData();
  //   formData.append('template', templateFile);
  //   formData.append('example', exampleFile);
  
  //   try {
  //     const response = await fetch('http://backend:5001/process', {
  //       method: 'POST',
  //       body: formData
  //     });
  //     if (!response.ok) {
  //       throw new Error('Network response was not ok');
  //     }
  //     const data = await response.json();
  //     setBackendData(data.report); // Accessing the report property from the backend response
  //   } catch (error) {
  //     console.error('There was a problem with the fetch operation:', error);
  //   }
  // };

  const formatInconsistencies = (report) => {
    const parts = report.split('----------------------\n');
    return parts.map((part, index) => {
      if (part.trim()) {
        const templateMatch = part.match(/template inconsistency \d+:\n([\s\S]*?)\nexample inconsistency \d+:\n/);
        const exampleMatch = part.match(/example inconsistency \d+:\n([\s\S]*)/);

        const templateInconsistency = templateMatch ? templateMatch[1].trim() : '';
        const exampleInconsistency = exampleMatch ? exampleMatch[1].trim() : '';

        return (
          <div key={index} className="inconsistency-block">
            <div className="template-inconsistency">
              <strong>Template Clause:</strong>
              <pre>{templateInconsistency}</pre>
            </div>
            <div className="example-inconsistency">
              <strong>Example Clause Inconsistency Detected:</strong>
              <pre>{exampleInconsistency}</pre>
            </div>
            {/* <div className="diff">
              <strong>Inconsistency Detected:</strong>
            </div> */}
          </div>
        );
      }
      return null;
    });
  };

  return (
    <div className="App">
      <h1>Business Contract Validation</h1>
      <div className="subheadings">
        <div className="subheading">
          <h2>Contract</h2>
          <p>(Select the file for which you wish to detect the inconsistency)</p>
          <input type="file" accept="application/pdf" onChange={handleExampleFileChange} />
        </div>
        <div className="subheading">
          <h2>Template</h2>
          <p>(The template against which you wish to check the contract PDF)</p>
          <input type="file" accept="application/pdf" onChange={handleTemplateFileChange} />
        </div>
      </div>
      <button className="submit-button" onClick={handleSubmit} disabled={loading}>
        {loading ? <div className="spinner"></div> : 'Submit'}
      </button>
      {backendData && (
        <div className="backend-data">
          {formatInconsistencies(backendData)}
        </div>
      )}
    </div>
  );
}

export default App;
