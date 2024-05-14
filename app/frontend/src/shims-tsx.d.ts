import { DefineComponent } from "vue";

declare global {
  namespace JSX {
    // tslint:disable no-empty-interface
    interface Element extends HTMLElement {}
    // tslint:disable no-empty-interface
    interface ElementClass extends DefineComponent {}
    interface IntrinsicElements {
      [elem: string]: any;
    }
  }
}
