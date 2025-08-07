import { useState } from 'react';
import axios from 'axios';

function Generate() {
  const [useOwnStory, setUseOwnStory] = useState(false);
  const [prompt, setPrompt] = useState('');
  const [title, setTitle] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [progress, setProgress] = useState([]);
  const [showProgressModal, setShowProgressModal] = useState(false);

  const placeholderText = useOwnStory
    ? "Enter your own story and our AI Story Maker will generate a video. If you want AI to help you write a story, click 'generate for me'."
    : "Enter a prompt or a story idea and our AI Story Maker will generate a full story. If you have your own story already, click 'Use my own story'.";

  const handleSubmit = async () => {
    setLoading(true);
    setResult(null);
    setProgress([]);
    setShowProgressModal(true);

    const storyId = 'story_' + Date.now();
    const ws = new WebSocket('ws://localhost:8000/ws/generate/');

    ws.onopen = () => {
      ws.send(JSON.stringify({
        prompt:prompt,
        user_story_title: useOwnStory ? title : null,
        story_id: storyId,
        is_custom_story: useOwnStory
      }));
    };

    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        if (parsed.type === 'final') {
          setResult({
            success: true,
            story_title: parsed.data.title,
            final_video_ui: parsed.data.final_video_ui
          });
          setShowProgressModal(false);
          setShowModal(true);
          setLoading(false);
        } else if (parsed.type === 'error') {
          setProgress((prev) => [...prev, `❌ Error: ${parsed.message}`]);
          setShowProgressModal(false);
          setLoading(false);
          ws.close();
        }
      } catch (e) {
        // It's a progress message (plain text)
        setProgress((prev) => [...prev, event.data]);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setProgress((prev) => [...prev, '❌ WebSocket error.']);
      setShowProgressModal(false);
      setLoading(false);
      ws.close();
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };
  };

  return (
    <div
      id="main"
      className="bg-[url(assets/images/generatepage.png)] bg-no-repeat w-screen h-screen bg-cover flex items-center justify-center"
    >
      <div className="text-white max-w-2xl text-center">
        {useOwnStory && (
            <input
                type="text"
                placeholder="Enter your story title or leave it blank for ai title generation"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-[600px] p-4 mb-4 rounded-md bg-gray-900 bg-opacity-50 border border-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-orange-500 placeholder-white placeholder-opacity-80 text-lg"
            />
            )}
            
        <textarea
          placeholder={placeholderText}
          name="message"
          rows={6}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="w-[600px] p-4 rounded-md bg-gray-900 bg-opacity-50 border border-gray-400 text-white mb-6 resize-none focus:outline-none focus:ring-2 focus:ring-orange-500 placeholder-white placeholder-opacity-80 text-lg min-h-[300px]"
        ></textarea>

        <div className="flex justify-center items-center gap-4 mb-6">
          <span className="text-base-sm">Generate for me</span>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              className="sr-only peer"
              checked={useOwnStory}
              onChange={() => setUseOwnStory(!useOwnStory)}
            />
            <div className="w-20 h-8 bg-blue-500 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:bg-green-600 after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border after:rounded-full after:h-7 after:w-7 after:transition-all peer-checked:after:translate-x-12"></div>
          </label>
          <span className="text-base-sm">Use my own story</span>
        </div>

        <div className="flex justify-center">
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-[300px] h-[60px] text-xl bg-[#f23711] text-white shadow-lg shadow-orange-700 rounded-md hover:bg-transparent hover:text-white border-2 border-[#ce2b07] transition duration-500"
          >
            {loading ? 'Generating...' : 'GENERATE NOW'}
          </button>
        </div>

        {/* Progress Spinner Modal */}
        {showProgressModal && (
          <div className="fixed inset-0 z-40 flex items-center justify-center bg-black bg-opacity-70">
            <div className="bg-gray-800 p-8 rounded-lg text-white text-center max-w-md w-full">
              <div className="flex justify-center mb-4">
                <div className="w-12 h-12 border-4 border-orange-400 border-t-transparent rounded-full animate-spin"></div>
              </div>
              <h2 className="text-xl font-semibold mb-2">Generating...</h2>
              <div className="text-left max-h-40 overflow-y-auto text-sm border-t border-gray-600 pt-2">
                {progress.map((msg, idx) => (
                  <div key={idx}>• {msg}</div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Final Video Modal */}
        {showModal && result && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80">
            <div className="relative w-[90vw] max-w-4xl bg-gray-900 rounded-lg shadow-lg p-6 text-white">
              <button
                className="absolute top-4 right-4 text-white bg-red-600 hover:bg-red-700 px-3 py-1 rounded"
                onClick={() => setShowModal(false)}
              >
                ✕
              </button>

              {result.success ? (
                <>
                  <h2 className="text-2xl font-bold mb-4">Story Generated!</h2>
                  <p className="mb-4 text-lg">Title: {result.story_title}</p>
                  <video
                      key={result.final_video_ui} // ensures React resets it properly
                      controls
                      className="w-full rounded-lg"
                      crossOrigin="anonymous"
                      src={result.final_video_ui}
                    />
                </>
              ) : (
                <p className="text-red-400 text-lg">Error: {result.error}</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Generate;
