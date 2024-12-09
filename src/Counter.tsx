import type { Component } from "solid-js";
import { createSignal, createEffect } from "solid-js";

// import logo from "./logo.svg";
// import styles from "./App.module.css";

type CounterProps = {
  initialCount?: number;
};

const Counter: Component<CounterProps> = (props) => {
  const [count, setCount] = createSignal(props.initialCount || 0);
  const increment = () => {
    console.log(`increment (before): ${count()}`);
    setCount((prev) => {
      console.log(`increment (prev): ${prev}`);
      return prev + 1;
    });
    console.log(`increment (after): ${count()}`);
  };

  (() => {
    let effectCount = 0;
    createEffect(() => {
      effectCount++;
      console.log(`effect called: ${effectCount} times`);
      if (effectCount > 0) {
        console.log(`count (effect): ${count()}`);
      }
    });
  })();

  return (
    <div>
      <div>Count {count()}</div>
      <div>
        <button type="button" onClick={increment}>
          Increment
        </button>
      </div>
    </div>
  );
};

export default Counter;

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
