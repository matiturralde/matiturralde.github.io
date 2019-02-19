import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Form, Grid, Label } from 'semantic-ui-react'
import sha1 from 'crypto-js/sha256'
import Base64 from 'crypto-js/enc-base64'
import { savePassAction } from './accions'

export class Step3 extends Component {
    state = {
        inputPass: null,
        inputRep: null,
        _loading: false,
        redirectToReferrer: false,
        showMessage: false,
        message: ''
    }
  
    static propTypes = {
        handleSavePass: PropTypes.func,
        email: PropTypes.any,
        message: PropTypes.any
    }

    static defaultProps = {
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
            inputPass,
            inputRep,
        } = this.state

        const {
            email
        } = this.props

        let errors = true

        if (inputRep !== null && inputPass !== null && inputRep === inputPass && inputPass.length > 5 && /[a-z]/.test(inputPass) && /[0-9]/.test(inputPass)) {
            errors = false
        }

        if (!errors) {
            const hashDigest = sha1(inputPass);

            const hmacDigest = Base64.stringify(hashDigest);

            this.props.handleSavePass({
                email: email,
                password: hmacDigest
            })

            this.setState({
                _loading: true
            })
        } else {
            this.setState({
                message: 'Las contraseñas debes ser iguales y contener por lo menos 6 caracteres, una letra y un número.',
                showMessage: true
            })
        }       

    }

  handleChange = (e, { name, value }) => this.setState({ [name]: value })

  render() {
        const {
            _loading,
            redirectToReferrer,
            showMessage,
            message
        } = this.state

        const title = '¡Confirmación de email exitosa!'
        const text = 'Necesitamos que elijas una contraseña para que tus datos queden guardados de forma segura.'

        if (redirectToReferrer) {
            return <Redirect to={{pathname: '/step4'}} />;
        }

        return (
            <Grid centered>
                <Grid.Column width={10}>
                    <Form onSubmit={this.handleSubmit} loading={_loading}>
                        <h2 style={{color: '#092768'}}> { title } </h2>
                        <p>
                            { text }
                        </p>
                        
                        <br />
                        <Form.Input
                            label='Contraseña'
                            placeholder='Contraseña'
                            name='inputPass'
                            onChange={this.handleChange}
                            type='password'
                            required
                        />
                        <Form.Input
                            label='Repetir Contraseña'
                            placeholder='Repetir Contraseña'
                            name='inputRep'
                            onChange={this.handleChange}
                            type='password'
                            required
                        />
                        <br />
                        <Button type='submit' style={{color: '#fff', background: '#EE3A43'}}>Continuar</Button>
                    </Form>
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
    email: state.step1Reducer.email,
    message: state.step3Reducer.messageStep3,
})

const mapDispatchToProps = (dispatch) => ({
    handleSavePass: (payload) => dispatch(savePassAction(payload)),
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step3))