import type { Component } from "solid-js";
import * as Tone from "tone";

import {
  //createContext,
  //useContext,
  createSignal,
  onMount,
  //createEffect,
} from "solid-js";

//// import logo from "./logo.svg";
//// import styles from "./App.module.css";
//type CounterProps = {
//  initialCount?: number;
//};
//
//type MyContextType = {
//  count: () => number; // Signal getter for count
//  setCount: (value: number) => void; // Signal setter for count
//};
//
//const MyContext = createContext<MyContextType | null>(); // es-lint-disable-line no-unused-vars
//
//const CounterLabel: Component = () => {
//  const context = useContext(MyContext);
//  if (!context) {
//    throw new Error("CounterLabel must be used within a Counter");
//  }
//
//  const { count, setCount: _ } = context;
//
//  return (
//    <div>
//      Counter Label: <code>{count()}</code>
//    </div>
//  );
//};
//
//const CounterButton: Component = () => {
//  const context = useContext(MyContext);
//  if (!context) {
//    throw new Error("CounterButton must be used within a Counter");
//  }
//
//  const { setCount } = context;
//
//  console.log(`context: ${context}`);
//  console.log(context);
//  console.log(`setCount: ${setCount}`);
//
//  return (
//    <button type="button" onClick={() => setCount((prev) => prev + 1)}>
//      Increment
//    </button>
//  );
//};

const ToneButton: Component = () => {
  //const [count, setCount] = createSignal(props.initialCount || 0);
  //const increment = () => {
  //  console.log(`increment (before): ${count()}`);
  //  setCount((prev) => {
  //    console.log(`increment (prev): ${prev}`);
  //    return prev + 1;
  //  });
  //  console.log(`increment (after): ${count()}`);
  //};
  //
  //(() => {
  //  let effectCount = 0;
  //  createEffect(() => {
  //    effectCount++;
  //    console.log(`effect called: ${effectCount} times`);
  //    if (effectCount > 0) {
  //      console.log(`count (effect): ${count()}`);
  //    }
  //  });
  //})();

  //<div>Count {count()}</div>
  //<div>
  //  <button type="button" onClick={increment}>
  //    Increment
  //  </button>
  //</div>

  //const [count, setCount] = createSignal(0);
  //const value = { count, setCount };

  const [isPlaying, setIsPlaying] = createSignal(false);

  onMount(async () => {
    await Tone.start(); // Unlock the Web Audio API when the app is loaded
    console.log("Audio context started!");
  });

  const playTone = () => {
    //await Tone.start(); // Unlock the audio context
    const synth = new Tone.Synth().toDestination(); // Create a synth and connect it to the master output
    synth.triggerAttackRelease("C4", "8n"); // Play a single note (C4) for an eighth note duration
    setIsPlaying(true);
    setTimeout(() => setIsPlaying(false), 500); // Reset after playback
  };

  return (
    <button
      onClick={playTone}
      disabled={isPlaying()}
      style={{
        padding: "10px 20px",
        "font-size": "16px",
        cursor: isPlaying() ? "not-allowed" : "pointer",
      }}
    >
      {isPlaying() ? "Playing..." : "Play Tone"}
    </button>
  );
};

export default ToneButton;

//<header class={styles.header}>
//  <img src={logo} class={styles.logo} alt="logo" />
//  <p>
//    Edit <code>src/App.tsx</code> and save to reload.
//  </p>
//  <p>
//    This is the beginning of a <i>new</i> app by Adrien Treuille
//  </p>
//  <p>
//    <svg height="300" width="400">
//      <defs>
//        <linearGradient id="gr1" x1="0%" y1="60%" x2="100%" y2="0%">
//          <stop
//            offset="5%"
//            style="stop-color:rgb(255,255,3);stop-opacity:1"
//          />
//          <stop
//            offset="100%"
//            style="stop-color:rgb(255,0,0);stop-opacity:1"
//          />
//        </linearGradient>
//      </defs>
//      <ellipse cx="125" cy="150" rx="100" ry="60" fill="url(#gr1)" />
//      Sorry but this browser does not support inline SVG.
//    </svg>
//  </p>
//  <a
//    class={styles.link}
//    href="https://github.com/solidjs/solid"
//    target="_blank"
//    rel="noopener noreferrer"
//  >
//    Learn Solid
//  </a>
//</header>
