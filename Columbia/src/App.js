import React, { Component } from 'react';
import { Container, Icon } from 'semantic-ui-react'
import AppRoutes from './routes'
import { connect } from 'react-redux'
import { cleanStore } from './localStore'
import { withRouter } from 'react-router-dom'
import PropTypes from 'prop-types'

import './App.css';
import 'semantic-ui-css/semantic.min.css'

import { Button } from 'semantic-ui-react'


class App extends Component {
  state = {
    isLoggerdIn: false
  }

  static propTypes = {
    isLoggerdIn: PropTypes.bool
  }

  static defaultProps = {
    isLoggerdIn: false
  }

  componentWillMount() {
    const {
      isLoggerdIn
    } = this.props;

    if (isLoggerdIn) {
      this.setState({
        isLoggerdIn
      })  
    }
  }

  componentWillReceiveProps(nextProps) {
    const {
        isLoggerdIn
    } = nextProps;

    this.setState({
        isLoggerdIn
    })
  }

  handleLogout = () => {
    cleanStore()
  }

  render() {
    const {
      isLoggerdIn
    } = this.state
    
    return (
      <div className="App">
        <header className="App-header">
          <img src='https://hbsrv.bancocolumbia.com.ar/images/logo.png' className="App-logo" alt="logo" />
          <div className="App-title">
            {
              isLoggerdIn ? (
                <div align="right">
                  <Button basic onClick={this.handleLogout} color='orange'><Icon name='sign out' />Guardar y salir</Button>
                </div>
              ) : (
                <span />
              )
            }
          </div>
        </header>
        <br />
        <Container textAlign='left'>
          <AppRoutes isLoggerdIn={isLoggerdIn}/>  
        </Container>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  isLoggerdIn: state.loginReducer.isLoggerdIn
})

const mapDispatchToProps = () => ({
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(App))
