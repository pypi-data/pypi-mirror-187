if (typeof loadPyodide === 'undefined') {
    let script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.21.3/full/pyodide.js';
    script.onload = async () => {
        let pyodide = await loadPyodide();
        window.pyodide = pyodide;
        pyodide.runPythonAsync(`# python replace marker`);
    };
    document.body.append(script)
}