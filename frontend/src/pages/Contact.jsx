import React from 'react';

function Contact() {
  return (
    <div class="min-h-screen w-full bg-[url('assets/images/aboutpage.png')] bg-cover bg-no-repeat bg-center px-6 py-12 flex items-center">
      <div
        id="contact"
        className="flex items-center justify-center"
      >
        <h1 className="text-3xl font-bold text-center text-blue-700 mb-6">
          CONTACT US
        </h1>
        <form className="flex flex-col space-y-4">
          <input
            type="text"
            placeholder="Full Name"
            required
            className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="email"
            placeholder="Type Your E-Mail"
            required
            className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            name="message"
            placeholder="Write Here..."
            required
            rows="5"
            className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
          <input
            type="submit"
            value="Send"
            className="bg-blue-600 text-white font-semibold py-2 rounded-md hover:bg-blue-700 cursor-pointer transition"
          />
        </form>
      </div>
    </div>
  );
}

export default Contact;
