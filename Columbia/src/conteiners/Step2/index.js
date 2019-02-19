import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Form, Grid, Label } from 'semantic-ui-react'
import { getPinAction, sentPinAction } from './accions'

export class Step2 extends Component {
    state = {
        inputPin: '',
        showMessage: false,
        showSentMessage: false,
        message: '',
        redirectToReferrer: false
    }
  
    static propTypes = {
        handleValidatePin: PropTypes.func,
        handleReSentPin: PropTypes.func,
        pin: PropTypes.any,
        email: PropTypes.any,
        message: PropTypes.any
    }

    static defaultProps = {
        pin: '',
        email: '',
        message: ''
    }

    componentWillReceiveProps(nextProps) {
        const {
            message
        } = nextProps;

        if (message !== 'done') {
            this.setState({
                message: message,
                showMessage: true,
                _loading: false
            })
        } else {
            this.setState({
                redirectToReferrer: true,
            })
        }

    }

    handleSubmit = () => {
        const {
            inputPin
        } = this.state

        const { email } = this.props

        if (inputPin !== '') {
            this.props.handleValidatePin({
                email: email,
                pin: inputPin
            })
            
            this.setState({
                _loading: true
            })
        }
    }

    handleChange = (e, { name, value }) => this.setState({ [name]: value })

    handleReSent = () => {
        const {
            email
        } = this.props

        this.props.handleReSentPin({
            email: email
        })

        this.setState({
            showSentMessage: true
        })
    }

    render() {
    const {
        redirectToReferrer,
        showMessage,
        showSentMessage,
        _loading,
        message
    } = this.state
    
    const title = 'Confirmación de email'
    const textInformative = 'Por favor ingresá el código que te enviamos a la dirección de email que nos indicaste. Asegurate de que no haya llegado a Correo No Deseado.'

    if (redirectToReferrer) {
        return <Redirect to={{pathname: '/step3'}} />;
    }

    return (
      <Grid centered>
                <Grid.Column width={10}>
                    <h2 style={{color: '#092768'}}> { title } </h2>
                    <Form onSubmit={this.handleSubmit} loading={_loading}>
                        <p>
                            { textInformative  }
                        </p>
                        <Form.Input
                            label='Pin'
                            placeholder='Pin'
                            name='inputPin'
                            onChange={this.handleChange}
                            type='input'
                            required
                        />
                        <p>
                            ¿No recibiste el Pin? <a onClick={this.handleReSent}> Enviar de nuevo. </a>
                        </p>
                        {
                            showSentMessage ? (
                                <p>
                                    <Label color='green' key='red'>
                                        Se re envio Pin
                                    </Label>
                                </p>
                            ) : (
                                <p>
                                    <span />
                                </p>                                
                            )
                        }
                        <Button type='submit' style={{color: '#fff', background: '#EE3A43'}}>Continuar</Button>
                    </Form>
                    <br />
                    {
                        showMessage ? (
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
    email: state.step1Reducer.email,
    message: state.step2Reducer.messageStep2,
})

const mapDispatchToProps = (dispatch) => ({
    handleValidatePin: (payload) => dispatch(getPinAction(payload)),
    handleReSentPin: (payload) => dispatch(sentPinAction(payload)),
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step2))
