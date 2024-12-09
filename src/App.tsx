import type { Component } from "solid-js";

import Counter from "./Counter";

import logo from "./logo.svg";
import styles from "./App.module.css";

const App: Component = () => {
  return (
    <div class={styles.App}>
      <header class={styles.header}>
        <img src={logo} class={styles.logo} alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <p>
          This is the beginning of a <i>new</i> app by Adrien Treuille
        </p>
        <p>
          <Counter initialCount={11} />
        </p>
        <a
          class={styles.link}
          href="https://github.com/solidjs/solid"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn Solid
        </a>
      </header>
    </div>
  );
};

export default App;

//<p>
//  <!--
//  <svg height="300" width="400">
//    <defs>
//      <linearGradient id="gr1" x1="0%" y1="60%" x2="100%" y2="0%">
//        <stop
//          offset="5%"
//          style="stop-color:rgb(255,255,3);stop-opacity:1"
//        />
//        <stop
//          offset="100%"
//          style="stop-color:rgb(255,0,0);stop-opacity:1"
//        />
//      </linearGradient>
//    </defs>
//    <ellipse cx="125" cy="150" rx="100" ry="60" fill="url(#gr1)" />
//    Sorry but this browser does not support inline SVG.
//  </svg>
//  -->
