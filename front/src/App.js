import React, { Component } from 'react';
import './App.css';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel'
import Divider from '@material-ui/core/Divider'
import Picker from 'emoji-picker-react';
 

class App extends Component {
  onEmojiClick = (event, emojiObject) => {
    event.preventDefault();

    this.setState({short: this.state.short+emojiObject.emoji})
  }
  
  handleChange(event) {
    const n = event.target.name
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    this.setState({[n]: value})
  }


  constructor(props) {
    super(props);
    this.state = {short: "", oneshot: false, url: "", result: "", message: "Your URL"}
  }

   submitAndUpdate(endpoint) {
    fetch(endpoint, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({url: this.state.url, short: this.state.short, oneshot: this.state.oneshot})
        }).then((response) => response.json())
          .then((responseJson) => {
            this.setState({result: responseJson.result, message: responseJson.message});
          })
          .catch((error) => {
            //console.error(error);
            this.setState({result: "Failed to request data :(", message: "Your URL"});
          });
   }
  
  onSubmit = (e) => {
    e.preventDefault();
    this.submitAndUpdate('/make')
  }
  
  simpleEncode(e) {
    e.preventDefault();
    this.submitAndUpdate('/encode')
  }
  
  testURL() {
    return /^(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?$/;
  }
  

  render() {
    return (
      <Container maxWidth="sm">
        <form onSubmit={this.onSubmit}>
          <Grid container><TextField name="url" margin="normal"  error={!this.testURL().test(this.state.url)} fullWidth label="URL" variant="outlined" value={this.state.url} onChange={this.handleChange.bind(this)}/></Grid>
          <Grid container alignItems="flex-start" justify="flex-end" direction="row"><Button id="encode" disabled={!this.state.url} onClick={this.simpleEncode.bind(this)} variant="contained">Encode</Button></Grid>
          <Grid container><TextField margin="normal" fullWidth id="short" label="Short" variant="outlined" name="short" value={this.state.short} onChange={this.handleChange.bind(this)}/></Grid>
          <Grid container alignItems="flex-start" justify="flex-end" direction="row"><Picker onEmojiClick={this.onEmojiClick}/></Grid>
          <Grid container><FormControlLabel label="One Time Link" name="oneshot" onChange={this.handleChange.bind(this)} control={<Checkbox id="oneshot" color="primary" />}/></Grid>
          <Grid container alignItems="flex-start" justify="flex-end" direction="row"><Button id="create" disabled={!(this.state.url && this.state.short)}type="submit" variant="contained" color="primary">Create</Button> </Grid>
        </form>
        <br />
        <Divider  margin="normal" />
        <Grid container><TextField id="result" label={this.state.message} variant="outlined" value={this.state.result} InputProps={{readOnly: true}} fullWidth margin="normal"/></Grid>
      </Container>
    );
  }
}

export default App;
