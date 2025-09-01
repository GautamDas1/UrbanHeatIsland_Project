import React from "react";

const Contact = () => {
  return (
    <section className="bg-white p-8 rounded-2xl shadow-lg border border-gray-200 mx-auto max-w-4xl my-20 font-sans">
      <h2 className="text-4xl font-bold mb-4 text-indigo-700 font-serif">📞 Contact Us</h2>
      <p className="text-gray-700 text-lg mb-4">
        Have questions, suggestions, or feedback? We'd love to hear from you!
      </p>
      <ul className="text-gray-600 text-md space-y-2">
        <li>📧 Email: <a className="text-indigo-600" href="mailto:uhi.support@example.com">uhi.support@example.com</a></li>
        <li>🌐 Website: <a className="text-indigo-600" href="https://uhi-visualizer.in">https://uhi-visualizer.in</a></li>
        <li>📍 Location: Bengaluru, India</li>
      </ul>
    </section>
  );
};

export default Contact;
