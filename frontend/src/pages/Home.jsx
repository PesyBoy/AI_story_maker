import React from 'react'
import { Link } from 'react-router-dom';

const Home = () => {
  return (
        <div id = 'main' class="bg-[url(assets/images/homepage.png)] bg-no-repeat
           w-screen h-screen bg-cover bg-relative flex items-center">
            <div className="fixed left-[-5%] top-[60%] transform -translate-y-1/2 text-white ml-[15%] max-w-2xl text-center">
              <h2 className="text-2xl md:text-4xl font-semibold mb-2 ">GOT A STORY IDEA?</h2>
              <h1 className="text-4xl md:text-5xl font-bold mb-4">BRING IT 
                <span className="text-[#f23711]"> TO LIFE</span> WITH AI</h1>
              <p className="text-lg mb-6"> Generate videos and audios for your stories</p>
              <div className="flex justify-center ">
                <Link to="/generate"
                 className='w-[300px] h-[60px] flex justify-center 
                 items-center text-xl bg-[#f23711] text-white shadow-lg 
                 shadow-orange-700 rounded-md hover:bg-transparent 
                 hover:text-white border-2 border-[#ce2b07] transition duration-500'>GENERATE NOW</Link>
              </div>

            </div>

        </div>


  )
}
export default Home;