import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Form, Grid, Label } from 'semantic-ui-react'
import { saveDataAction } from './accions'
import Steps from '../../components/Steps'

export class Step5 extends Component {
    state = {
        lastName: '',
        name: '',
        phone: '',
        showMessage: false,
        message: '',
        redirectToReferrer: false
    }
  
    static propTypes = {
        handleSave: PropTypes.func,
        email: PropTypes.any,
        message: PropTypes.any,
        isSociety: PropTypes.bool
    }

    static defaultProps = {
        email: '',
        message: '',
        isSociety: false
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
                redirectToReferrer: true
            })
        }

    }

    handleSubmit = () => {
        const {
            lastName,
            name,
            phone
        } = this.state

        const {
            email
        } = this.props

        if (lastName !== '' && name !== '' && phone !== '') {
            const nameComplete = `${lastName} ${name}`
            this.props.handleSave({
                email,
                name: nameComplete,
                phone
            })

            this.setState({
                _loading: true
            })
        } else {
            alert('Debe completar campos obligatorios (*)')
        }        
        
    }

    handleChange = (e, { name, value }) => this.setState({ [name]: value })

    render() {
    const {
        redirectToReferrer,
        showMessage,
        _loading,
        message
    } = this.state;

    const {
        isSociety
    } = this.props
    
    const title = 'Número de contacto'
    const textInformative = '¿Podés dejarnos por favor tu nombre y un teléfono por si tenemos que contactar para ayudarte en algún momento?'
    const text2 = '¡Prometemos no molestarte con ofertas!'

    if (redirectToReferrer) {
        return <Redirect to={{pathname: '/step6'}} />
    }

    return (
        <Grid centered>
            <Grid.Row stretched>
                <Grid.Column>
                    <Steps step={1} rSocial={isSociety}/>
                </Grid.Column>
            </Grid.Row>
            <Grid.Row>
                <Grid.Column width={10}>
                    <Form onSubmit={this.handleSubmit} loading={_loading}>
                        <h2 style={{color: '#092768'}}>
                            {title}
                        </h2>
                        <p>
                            { textInformative  }
                        </p>
                        <p>
                            { text2  }
                        </p>
                        <Form.Input
                            label='Apellido'
                            placeholder='Apellido'
                            name='lastName'
                            onChange={this.handleChange}
                            type='input'
                            required
                        />
                        <Form.Input
                            label='Nombre'
                            placeholder='Nombre'
                            name='name'
                            onChange={this.handleChange}
                            type='input'
                            required
                        />
                        <Form.Input
                            label='Telefono'
                            placeholder='Teléfono'
                            name='phone'
                            onChange={this.handleChange}
                            type='input'
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
            </Grid.Row>
        </Grid>
    )
  }
}

const mapStateToProps = (state) => ({
    email: state.step1Reducer.email,
    message: state.step5Reducer.messageStep5,
    isSociety: state.step4Reducer.isSociety,
})

const mapDispatchToProps = (dispatch) => ({
    handleSave: (payload) => dispatch(saveDataAction(payload)),
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step5))