import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Form, Grid, Label, Checkbox } from 'semantic-ui-react'
import { saveDataAction } from './accions'

export class Step4 extends Component {
    state = {
        valueCheckbox: '',
        cuit: '',
        rsocial: '',
        website: '',
        fanPage: '',
        linkedIn: '',
        twitter: '',
        _loading: false,
        redirectToReferrer: false,
        showMessage: false,
        message: ''
    }
  
    static propTypes = {
        handleSave: PropTypes.func,
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
                redirectToReferrer: true
            })
        }

    }

    handleSubmit = () => { 
        const {
            cuit,
            rsocial,
            website,
            fanPage,
            linkedIn,
            twitter,
            valueCheckbox
        } = this.state

        const {
            email
        } = this.props

        if (cuit !== '' && cuit.length < 12 && valueCheckbox !== '') {
            this.props.handleSave({
                email,
                cuit,
                rsocial,
                website,
                fanPage,
                linkedIn,
                twitter,
                valueCheckbox
            })
            
            this.setState({
                _loading: true
            })
        } else {
            alert('Debe completar campos requeridos (*) y el Cuit debe tener una longitud de 11 caracteres sin guiones ni espacios.')
        }
    }

    handleChange = (e, { name, value }) => this.setState({ [name]: value })

    render() {
        const {
            valueCheckbox,
            _loading,
            redirectToReferrer,
            showMessage,
            message
        } = this.state

        const title = 'Contanos por favor un poco de tu negocio.'
        const text = 'Con el CUIT y las redes sociales que uses vamos a conocer más de tu empresa y podremos ofrecerte un mejor crédito.'

        if (redirectToReferrer) {
            return <Redirect to={{pathname: '/step5'}} />;
        }

        return (
            <Grid centered>
                <Grid.Column width={10}>
                    <Form onSubmit={this.handleSubmit} loading={_loading}>
                        <h2 style={{color: '#092768'}}>
                            {title}
                        </h2>
                        <p> { text } </p>
                        <br />
                        <Form.Group widths='equal'>
                            <Form.Input
                                label='CUIT del negocio'
                                placeholder='CUIT del negocio'
                                name='cuit'
                                onChange={this.handleChange}
                                type='input'
                                required
                            />
                            <Form.Input
                                label='Razón Social'
                                placeholder='Razón Social'
                                name='rsocial'
                                onChange={this.handleChange}
                                type='input'
                            />
                        </Form.Group>
                        <p>
                            Tipo: <span style={{color: '#db2828'}}>*</span>
                        </p>
                        <Form.Group widths='equal'>
                            <Form.Field>
                                <Checkbox
                                    label='Monotributo / Autónomo'
                                    name='valueCheckbox'
                                    value='Unipersonal o Monotributo'
                                    checked={valueCheckbox === 'Unipersonal o Monotributo'}
                                    onChange={this.handleChange}
                                />
                                </Form.Field>
                                <Form.Field>
                                <Checkbox
                                    label='Sociedad'
                                    name='valueCheckbox'
                                    value='S.A. o S.R.L.'
                                    checked={valueCheckbox === 'S.A. o S.R.L.'}
                                    onChange={this.handleChange}
                                />
                            </Form.Field>
                        </Form.Group>
                        
                        <br />
                        <Form.Input
                            placeholder='Website del negocio'
                            name='website'
                            onChange={this.handleChange}
                            type='input'
                        />
                        <Form.Input
                            placeholder='Fan Page'
                            name='fanPage'
                            onChange={this.handleChange}
                            type='input'
                        />
                        <Form.Input
                            placeholder='LinkedIn de la empresa'
                            name='linkedIn'
                            onChange={this.handleChange}
                            type='input'
                        />
                        <Form.Input
                            placeholder='Twitter de la empresa'
                            name='twitter'
                            onChange={this.handleChange}
                            type='input'
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
    message: state.step4Reducer.messageStep4,
})

const mapDispatchToProps = (dispatch) => ({
    handleSave: (payload) => dispatch(saveDataAction(payload)),
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step4))