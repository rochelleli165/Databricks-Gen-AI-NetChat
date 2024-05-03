import logo from './logo.svg';
import './App.css';
import {Button} from 'baseui/button';
import getInfo from './getInfo';
import React, {useState, useEffect } from "react";
import axios from 'axios';
import {Heading, HeadingLevel} from 'baseui/heading'
import { Input, SIZE } from 'baseui/input/';


import { Client as Styletron } from "styletron-engine-monolithic";
import { Provider as StyletronProvider } from "styletron-react";
import { LightTheme, DarkTheme, BaseProvider, styled } from "baseui";
import { StatefulInput } from "baseui/input";

const engine = new Styletron();

const Centered = styled("div", {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  height: "100%",
});

function App() {
  const [data, setData] = useState([]);

  
    const fetchData = async () => {
          try {
              const response = await axios.get('http://127.0.0.1:5000/api/getData');
              console.log(response.data);
              setData(response.data);
          } catch (error) {
              console.error('Error fetching data:', error);
          }
    };


     
  
  const [inputText, setInputText] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

    const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    
    // Add user message to chat history
    setChatHistory([...chatHistory, { sender: 'user', message: inputText }]);
    setInputText('');
    
    // Make request to your API to get ChatGPT response
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/getData?question=${inputText}`);
      // Add ChatGPT response to chat history
      setChatHistory([...chatHistory, { sender: 'chatbot', message: response.data }]);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const color = {
    color: "white",
  };

  const red = {
    backgroundColor: "#831010",
  };

  return (
    <StyletronProvider value={engine}>
      <BaseProvider theme={LightTheme}>
        <Centered>
            <HeadingLevel>
              <Heading  style={color} >NetChat</Heading>
          </HeadingLevel>
        </Centered>
        <main>
        <div className="chat-window">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.message}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="form">
        <Centered>
        <Input
            placeholder="Type your message..."
            value={inputText}
            size={SIZE.large}
            clearOnEscape
            onChange={handleInputChange}
          />
          <div className="padding"></div>
          <Button style={red}>Submit</Button>
          </Centered>
        </form>
        </main>
      </BaseProvider>
    </StyletronProvider>
     
  );
}

export default App;
