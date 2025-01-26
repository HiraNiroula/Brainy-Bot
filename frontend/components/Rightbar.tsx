"use client";
import React, { useState, useEffect } from "react";

const Rightbar = () => {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("...✋ Hello World ✋...");
  const [isLoading, setIsLoading] = useState(false);

  const buttons = [
    { name: "Subject" },
    { name: "ORM" },
    { name: "Voice Ars" },
    { name: "FAQ" },
  ];

  // Static content for prompts
  const staticContent = {
    "Health and Wellness":
      "Table of Contents ndiUnit 1 1 2: Business and Interest    Unit 3  ‘Health and Wellness   The unit consists of writing, screenplays, and group conversations ter: A letter from a  inpatient  Pre- atives)  Study the table showing how imperatives are changed ech and deliver in a group .  8.  heel chart and present .  12. Extra bit ads students  towards the theme of the unit, i.  a student to read out the dimensions mentioned on it.  ts of wellness namely emotional, environmental, financial, ls to our access to resources for personal development.   ort of your expectations, and for that, we are truly nding as we work towards improvements . To better Â ve any further questions or if there is anythin g specific tal Name and address]   ============3.7 p session introducing the reading text.  Instruct students  to Unit 5 : Science and Experiment    d   Unit 1 7: Countries and Towns   Â  arly, the listening and speaking activities aim to ew   S.N. Textbook ions .   Work in a group of three and sentences with the correct words from  the  text. tences.   10. Writing II: Gu sessments of students  after teaching  each   a. Introduce the unit and its theme to  their responses , and conclude the discussion with your feedback and environmental and financial factors also play a role in shaping ality care and ensuring a positive experience for our patients and ective measures are being implemented to enhance the overall quality of ing the ive made  necessary changes to ensure a rtunity to serve you better in the future.   a. To present the text in a speech .",
    "Food and Cuisine":
      "Table of Contents ndiUnit 1 1 2: Business and Interest    Unit 6    (Food and Cuisine   e erfunctions with activities that encourage students to enact eme of food, while an extra bit focuses on   tch the words with the correct meanings.   extingMatch 5.  Grammar I  Connectives: Reason the profile of Nepali cuisine globally.   I am ers can be rewarding as personal success.   Post e they are done, ask each group to share their  nd mastery of various culinary techniques.   For example e judges with a dish that   stands out e. Tell students  that the listening activity is based  Food science is in understanding how  food is produced, processed  the audio until students  complete the task.   ve to write whether the given statements are true or false. e  ͡     Unit 1 1: Culture and Interest    d    87    Unit 6   7   anguage functions with activities that encourage students to enact conversations the theme of food, while an extra bit focuses on  s   extingMatch the words with the correct meanings. ns.   1.5.  Grammar I evate the profile of Nepali cuisine globally.   o  Learning aboutothers can be rewarding as personal success e. Once they are done, ask each group to share ity inessand mastery of various culinary techniques.   ide the judges with a dish that  stands out cuisine. Tell students  that the listening activity is .   b. Food science is in understanding how d play the audio until students  complete the task. ill have to write whether the given statements are true or false e. True.",
  };

  // Function to fetch data from the API (optional)
  const fetchData = async () => {
    if (!prompt.trim()) return; // Don't call API with empty prompt

    setIsLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/summaries/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: prompt }),
      });
      const data = await res.json();
      // Update response with data from API or static content
      setResponse(
        data.summary || staticContent[prompt] || "No response received."
      );
    } catch (error) {
      setResponse("Error fetching response. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Handle prompt submission on Enter key press
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      fetchData();
    }
  };

  return (
    <div className="bg-gradient-to-r from-purple-200 to-gray-400 bg-[#B0A8A8] shadow-lg flex flex-col items-center gap-4 w-full rounded-lg h-[93%] px-4 py-3">
      {/* head */}
      <div className="flex justify-between w-full text-lg">
        <div className="flex items-center justify-center font-semibold text-xl gap-2">
          <img
            src="/brainy.png"
            className="w-7 h-7 rounded-full"
            alt="brainy"
          />
          <h1>Brainy Bot</h1>
        </div>
        <div className="flex gap-2 items-center justify-center">
          <button className="bg-gradient-to-r from-gray-300 to-purple-100 shadow-md bg-[#8D8C8C] text-base font-semibold border-black px-5 rounded-lg py-[6px]">
            Login
          </button>
          <button className="bg-gradient-to-r text-base from-gray-300 to-purple-100 shadow-md bg-[#8D8C8C] font-semibold border-black px-5 rounded-lg py-[6px]">
            SignUp
          </button>
        </div>
      </div>

      {/* Optional head */}
      <div className="flex self-start mx-[50px] gap-4">
        {buttons.map((data, index) => (
          <button
            className="bg-gradient-to-r from-purple-100 to-gray-300 bg-[#8D8C8C] shadow-md px-[5px] py-[8px] w-[100px] rounded-lg border-black font-semibold"
            key={index}
          >
            {data.name}
          </button>
        ))}
      </div>

      {/* ChatBox */}
      <div className="bg-gradient-to-r from-purple-100 to-gray-300 text-center flex items-center justify-center text-xl shadow-md w-[90%] h-full rounded-lg py-2 overflow-y-auto px-6 font-semibold overflow-hidden">
        {isLoading ? "⏳ Loading..." : response}
      </div>

      {/* Prompt Box */}
      <div className="bg-gradient-to-r from-purple-200 to-gray-200 shadow-md flex items-center justify-between w-[90%] bg-[#8D8C8C] rounded-lg py-4 px-3 overflow-hidden">
        <div className="flex items-center gap-3 justify-center">
          <img className="cursor-pointer" src="/mic.png" alt="microphone" />
          <input
            className="bg-transparent text-black placeholder:font-semibold placeholder-black outline-none border-none w-[100vh]"
            type="text"
            placeholder="Enter your prompts here..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyPress={handleKeyPress}
          />
        </div>
        <div className="flex items-center justify-center gap-3">
          <img
            className="cursor-pointer"
            src="/send.png"
            alt="send"
            onClick={fetchData}
          />
          <img className="cursor-pointer" src="/gif.png" alt="gif" />
          <img className="cursor-pointer" src="/image.png" alt="image" />
        </div>
      </div>
    </div>
  );
};

export default Rightbar;