import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { withRouter, Redirect } from 'react-router-dom'
import { connect } from 'react-redux'
import { Button, Grid, Header, Icon, Input, Label } from 'semantic-ui-react'
import { validationAction, cleanMessageAction } from './accions'

export class Login extends Component {
    state = {
        email: '',
        password: '',
        stepPath: '',
        message: '',
        _loading: false,
        _redirectTo: false,
        _redirectToRegister: false,
        showMessage: false
    }

    static propTypes = {
        validationAction: PropTypes.func,
        handleCleanMessage: PropTypes.func,
        message: PropTypes.any,
        redirect: PropTypes.any,
        isLoggerdIn: PropTypes.bool
    }

    static defaultProps = {
        message: '',
        redirect: '',
        isLoggerdIn: false
    }

    componentWillMount() {
        const {
            redirect,
            isLoggerdIn
        } = this.props;

        if (isLoggerdIn) {
            this.setState({
                stepPath: redirect,
                _redirectTo: true,
            })
        }        
    }

    componentWillReceiveProps(nextProps) {
        const {
            message,
            redirect
        } = nextProps;

        if (message !== 'done') {
            this.setState({
                message: message,
                showMessage: true,
                _loading: false
            })
        } else {
            this.setState({
                stepPath: redirect,
                _redirectTo: true,
            })
        }

    }

    handleChange = (e, { name, value }) => this.setState({ [name]: value })

    handleLogin = () => {
        const {
            email,
            password
        } = this.state

        this.props.handleValidate({
            email,
            password
        })

        this.setState({
            _loading: true
        })
    }

    handleRegister = () => {
        this.setState({
            _redirectToRegister: true
        })
    }

    render() {
        const {
            stepPath,
            _redirectTo,
            _redirectToRegister,
            _loading,
            showMessage,
            message
        } = this.state

        if (_redirectTo) {
            if (stepPath === 'step99') {
                return <Redirect to={{pathname: '/greeting'}} />
            } else {
                return <Redirect to={{pathname: stepPath}} />
            }            
        }
        
        if (_redirectToRegister) {
            return <Redirect to={{pathname: '/step1'}} />
        }

        const title = 'Gracias por volver!'
        const text = 'Por favor ingresá para continuar con tu solicitud.'

        return (
            <Grid centered>
                <Grid.Column width={8}>
                    <h2 style={{color: '#f9690e'}}> { title } </h2>    

                    <p> { text } </p>    
                                        
                    <Header as='h2'>
                        <Icon name='user circle' />
                        <Header.Content>Login</Header.Content>
                    </Header>                   
                    
                    <br />

                    <Input fluid iconPosition='left' placeholder='Email' name='email' onChange={this.handleChange}>
                    <Icon name='at' />
                        <input required/>
                    </Input>

                    <br />

                    <Input fluid iconPosition='left' placeholder='Password' name='password' onChange={this.handleChange}>
                    <Icon name='eye slash outline' />
                        <input type='password' required/>
                    </Input>

                    <br />

                    <Button fluid style={{color: '#fff', background: '#f9690e'}} onClick={this.handleLogin} loading={_loading}>Ingresar</Button>
                    
                    <br />

                    <p>
                        ¿Sos nuevo en Credility? <a href="/" >Registrate</a>
                    </p> 

                    <br />

                    {
                        showMessage && message !== '' ? (
                            <Label color='red' key='red'>
                                { message }  
                            </Label>
                        ) : (
                            <span />
                        )
                    }

                </Grid.Column>
            </Grid>
        )
    }
}

const mapStateToProps = (state) => ({
    message: state.loginReducer.messageLogin,
    redirect: state.loginReducer.stepRedirect,
    isLoggerdIn: state.loginReducer.isLoggerdIn
})

const mapDispatchToProps = (dispatch) => ({
    handleValidate: (payload) => dispatch(validationAction(payload)),
    handleCleanMessage: () => dispatch(cleanMessageAction()),
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Login))
