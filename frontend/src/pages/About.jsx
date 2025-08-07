import React from 'react'
import aboutimage from '../assets/images/aboutpage.png'

function About() {
  return (
<div class="min-h-screen w-full bg-[url('assets/images/aboutpage.png')] bg-cover bg-no-repeat bg-center px-6 py-12 flex items-center justify-center">
  <div class="max-w-4xl bg-black bg-opacity-50 p-10 rounded-xl shadow-lg backdrop-blur-md text-blue-400">
    <h1 class="text-4xl font-bold mb-6 text-orange-400">About the Technology</h1>
    <ul class="space-y-4 text-lg leading-relaxed">
      <li>
        <span class="text-blue-300 font-semibold">Story Generation:</span> We use <span class="text-orange-400 font-semibold">Mistral AI Large</span> to generate rich and engaging stories based on your prompt or uploaded content.
      </li>
      <li>
        <span class="text-blue-300 font-semibold">Scene Splitting & Prompting:</span> The same Mistral model is used to split the story into scenes and craft descriptive prompts for image generation.
      </li>
      <li>
        <span class="text-blue-300 font-semibold">Image & Video Generation:</span> We use <span class="text-orange-400 font-semibold">Stability AI</span> to generate stunning visuals and scenes from your story.
      </li>
      <li>
        <span class="text-blue-300 font-semibold">Voice Narration:</span> Audio is brought to life using <span class="text-orange-400 font-semibold">Coqui TTS (VITS model)</span>, delivering natural and expressive storytelling voices.
      </li>
      <li>
            <span className="text-blue-300 font-semibold">Database & Storage:</span> We use <span className="text-orange-400 font-semibold">Supabase</span> as our backend database and file storage solution. It securely manages user data, story metadata, and media files with real-time updates and authentication.
      </li>
    </ul>
  </div>
</div>


  )
}

export default About