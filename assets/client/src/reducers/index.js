import { combineReducers } from 'redux';
import notes from "./notes";
import auth from "./auth";


const userApp = combineReducers({
  notes, auth,
})

const rootReducer = (state, action) => {

  if ( action.type === 'AUTHENTICATION_ERROR') {
  state = undefined;
  }
  return userApp(state, action);
  }

export default rootReducer;