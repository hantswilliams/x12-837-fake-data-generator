# X12 837 Generator & Parser - Web Version (Pyodide)

A browser-based application that generates and parses X12 837 healthcare claim files using Python running in WebAssembly via Pyodide.

## Features

- **100% Client-Side**: No server required - everything runs in your browser
- **Cross-Platform**: Works on any device with a modern web browser
- **Easy Deployment**: Deploy to GitHub Pages, Netlify, Vercel, or any static hosting
- **No Installation**: Just open the HTML file in a browser

## How It Works

This application uses [Pyodide](https://pyodide.org/), which compiles Python to WebAssembly, allowing Python code to run directly in the browser. The application:

1. Loads Python runtime in the browser
2. Installs required packages (faker, pandas)
3. Runs the generator and parser Python code
4. Provides downloads for generated/parsed files

## Usage

### Local Development

Simply open `index.html` in a modern web browser:

```bash
cd web_pyodide
open index.html  # macOS
# or
start index.html  # Windows
# or
xdg-open index.html  # Linux
```

Or use a local server:

```bash
python -m http.server 8000
# Then open http://localhost:8000
```

### Deploying to GitHub Pages

1. **Push to GitHub**:
   ```bash
   git add web_pyodide/
   git commit -m "Add Pyodide web version"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository settings
   - Navigate to "Pages"
   - Source: Deploy from branch
   - Branch: `main`, folder: `/web_pyodide`
   - Save

3. **Access your app**:
   - Your app will be available at: `https://yourusername.github.io/your-repo-name/`

### Deploying to Netlify

1. **Drag and Drop**:
   - Go to [Netlify Drop](https://app.netlify.com/drop)
   - Drag the `web_pyodide` folder
   - Get instant deployment!

2. **Or use Netlify CLI**:
   ```bash
   cd web_pyodide
   netlify deploy --prod
   ```

### Deploying to Vercel

```bash
cd web_pyodide
vercel
```

## Features

### Generator Tab
- Generate 1-25 synthetic X12 837 files
- Download individual files
- Uses Faker library for realistic data

### Parser Tab
- Upload existing X12 837 files
- Extract claim and service data
- Download results as CSV files

## Browser Compatibility

Requires a modern browser with WebAssembly support:
- Chrome 57+
- Firefox 52+
- Safari 11+
- Edge 16+

## Performance Notes

- **First Load**: Takes 5-10 seconds to load Python and packages
- **Subsequent Operations**: Fast and responsive
- **Large Files**: Parser can handle files up to several MB

## Limitations

This is a simplified version that:
- Uses basic X12 generation (for demo purposes)
- Performs simplified parsing
- Runs in the browser (limited by browser memory)

For production use with full generator/parser logic, see the main project.

## Advantages Over Desktop Apps

1. **No Installation**: Works immediately in any browser
2. **Cross-Platform**: Same experience on Windows, macOS, Linux, mobile
3. **Easy Updates**: Just update the HTML/JS files
4. **Shareable**: Send a link instead of distributing installers
5. **Privacy**: All processing happens locally in the browser

## File Structure

```
web_pyodide/
├── index.html    # Main HTML page with UI
├── app.js        # JavaScript + Pyodide initialization
├── style.css     # Styling
└── README.md     # This file
```

## Customization

To use your full generator and parser code:

1. **Update `app.js`** - Replace the simplified generator/parser code with your actual code
2. **Load CSV Files** - Fetch and load your reference data files
3. **Adjust UI** - Modify HTML/CSS to match your needs

## Security

- All code runs client-side in the browser sandbox
- No data is sent to any server
- Files are processed locally and downloaded directly

## License

Same as the parent project.
