import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Generate from './pages/Generate';
import About from './pages/About';
import Contact from './pages/Contact';

function App() {
  return (
    // <div>I am this now</div>
    <Router>
      <Navbar />
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/generate" element={<Generate />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
      </Routes>
     </Router>
  );
}

export default App;