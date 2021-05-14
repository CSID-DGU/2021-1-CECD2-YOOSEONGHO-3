import { createStore, applyMiddleware,compose } from '@reduxjs/toolkit';
import thunk from "redux-thunk";
import rootReducer from './_reducers';


const store = createStore(
    rootReducer,
    compose(
      applyMiddleware(thunk),
      window.devToolsExtension ? window.devToolsExtension() : f => f
    )
  );
export default store;

