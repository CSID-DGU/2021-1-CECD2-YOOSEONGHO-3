import { combineReducers} from 'redux';
import dialogReducer from './DialogReducer';


const rootReducer=combineReducers({
    dialog:dialogReducer
});

export default rootReducer;