import {useState,useEffect} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import AccessibilityNewIcon from '@material-ui/icons/AccessibilityNew';
import { useSelector,useDispatch } from 'react-redux';
import {logoutUser} from '../store/_actions/userActions';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
        background:'linear-gradient(45deg, #AACEE2 30%, #EDEDED 90%)',
      },
      menuButton: {
        marginRight: theme.spacing(2),
      },
      title: {
        flexGrow: 1,
      },
  }));
  
const myBar=makeStyles(AppBar);

  export default function ButtonAppBar() {
    const classes = useStyles();
    const isLogin=useSelector(state=>state.user.isLogin);
    const username=useSelector(state=>state.user.username);
    const dispatch=useDispatch();
  
    return (
      <div className={classes.root}>
        <myBar position="static">
          <Toolbar>
            <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu" href="#">
             <AccessibilityNewIcon></AccessibilityNewIcon>
            </IconButton>
            <Typography variant="h6" className={classes.title}>
              모복
            </Typography>
            {isLogin?(<>
             {username}님 환영합니다
             <Button color="inherit" onClick={()=>{
               dispatch(logoutUser());
             }}>Logout</Button>
            </>):(<>
              <Button  color="inherit" href="#Signin" >Login</Button>
              <Button  color="inherit" href="#Signup" >Signup</Button>
            </>)}
          </Toolbar>
        </myBar>
      </div>
    );
  }