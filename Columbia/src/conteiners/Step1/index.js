import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { withRouter, Redirect } from 'react-router-dom'
import { connect } from 'react-redux'
import { Button, Checkbox, Form, Select, Grid, Label } from 'semantic-ui-react'
import { sendAction, addMailAction, getDestination } from './accions'

import './step1.css'

export class Step1 extends Component {
    state = {
        amount: 50000,
        deadline: 6,
        colorButton6: '#EE3A43',
        colorButton12: '#838787',
        formattedMin: '',
        email: '',
        destination: '',
        checked: false,
        redirectToReferrer: false,
        errors: {
            email: false,
            destination: false
        },
        showMessage: false,
        message: '',
        _loading: false,
        _loadSelect: true,
        destinations: [],
        referral: 'Credility',
        vendedor: ''
    }
    
    static propTypes = {
        handleSendMail: PropTypes.func,
        handleEmail: PropTypes.func,
        handleDestination: PropTypes.func,
        message: PropTypes.any,
        destinations: PropTypes.array,
        isLoggerdIn: PropTypes.bool 
    }

    static defaultProps = {
        message: '',
        isLoggerdIn: false
    }    
    
    componentWillMount() {
        const {
            location
        } = this.props

        const {
            monto,
            plazo
        } = this.props.match.params

        if (location.pathname.length > 2) {
            if (monto && plazo && plazo === '12') {
                this.setState({
                    referral: 'Columbia',
                    amount: parseInt(monto, 10),
                    deadline: parseInt(plazo, 10),
                    colorButton6: '#838787',
                    colorButton12: '#EE3A43',
                }, () => {
                    this.simulateCredit()
                })
            } else {
                if (monto && plazo) {
                    this.setState({
                        referral: 'Columbia',
                        amount: parseInt(monto, 10),
                        deadline: parseInt(plazo, 10),
                    }, () => {
                        this.simulateCredit()
                    })
                } else {
                    this.setState({
                        referral: 'Columbia'
                    })
                }
            }            
        }

        this.simulateCredit()
        this.props.handleDestination()
    }

    componentWillReceiveProps(nextProps) {
        const {
            message,
            destinations
        } = nextProps;
        
        if (message !== 'done') {
            this.setState({
                redirectToReferrer: false,
                showMessage: true,
                message: message,
                _loading: false,
                _loadSelect: false,
                destinations
            })
         } else {
            this.setState({
                redirectToReferrer: true,
            })
         }
        
    }

    handleSubmit = () => {
        const {
            destination,
            email,
            checked,
            amount,
            deadline,
            referral,
            vendedor
        } = this.state

        if (destination !== 'Préstamo Personal' && destination !== 'Renovación de controladores fiscales' && destination !== '' && email !== '' && /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email) && checked) {
            this.props.handleEmail(email);
            this.props.handleSendMail({
                destination,
                email,
                amount,
                deadline,
                referral
            });

            this.setState({
                _loading: true
            })

        } else {
            if (destination === 'Renovación de controladores fiscales' && destination !== '' && email !== '' && checked && vendedor !== '') {
              this.props.handleEmail(email);
              this.props.handleSendMail({
                  destination,
                  email,
                  amount,
                  deadline,
                  referral,
                  vendedor
              });

              this.setState({
                  _loading: true
              })

            } else {
                if (destination === 'Préstamo Personal' && destination !== '' && email !== '' && checked) {
                    window.location.href = "https://www.credility.com/landing-personal?nuevo=true"
                } else {
                    alert('Debe completar todos los campos y aceptar terminos y condiciones.')
                }
            }                        
        }
    }

    handleChangecalculator = (e, { name, value }) => {
        this.setState({
            [name]: parseInt(value,10)
        }, () => {
            this.simulateCredit()
        })
    }

    handleChange = (e, { name, value }) => this.setState({ [name]: value })

    toggle = () => this.setState({ checked: !this.state.checked })

    currency = (value) => {
        var result = value.toFixed(0).replace(/./g, function (c, i, a) {
            return i && c !== "," && ((a.length - i) % 3 === 0) ? '.' + c : c
        });
        return result
    }

    handleChange6 = () => {
        this.setState({
            deadline: 6,
            colorButton6: '#EE3A43',
            colorButton12: '#838787',
        }, () => {
            this.simulateCredit()
        })
    }

    handleChange12 = () => {
        this.setState({
            deadline: 12,
            colorButton6: '#838787',
            colorButton12: '#EE3A43',
        }, () => {
            this.simulateCredit()
        })
    }

    simulateCredit = () => {
        let cuotaMin = ''

        switch (this.state.deadline) {
            case 6:
                cuotaMin = this.state.amount * 0.206577089589019
                break;
            case 12:
                cuotaMin = this.state.amount * 0.122245549919824
                break;
            default:
                break;
        }

        const formattedMin = this.currency(cuotaMin);

        this.setState({
            formattedMin
        })
    }

    render() {
        const {
            destination,
            amount,
            formattedMin,
            redirectToReferrer,
            errors,
            _loading,
            showMessage,
            message,
            destinations,
            _loadSelect,
            colorButton6,
            colorButton12
        } = this.state

        const textCalculator = `Tu cuota mensual promedio sería de AR$ ${formattedMin}`
        const textHead = '¡Vamos a empezar!'
        const text = 'Necesitamos que completes algunos datos para conocer más de tu negocio y poder hacerte una oferta de crédito. ¡Pero no te asustes! Son menos de 10 minutos de tu tiempo. Primero, contanos cuánto dinero estás necesitando y para qué lo vas a usar.'

        if (redirectToReferrer) {
            return <Redirect to={{pathname: '/step2'}} />;
        }

        return (
            <Grid centered>
                <Grid.Column width={10}>
                    <Form onSubmit={this.handleSubmit} loading={_loading}>
                        <h2 style={{color: '#092768'}}>
                            {textHead}
                        </h2>
                        <p>
                            {text}
                        </p>

                        <Form.Input
                            label='Email'
                            placeholder='Email'
                            name='email'
                            onChange={this.handleChange}
                            type='input'
                            required
                            error={errors.email}
                        />
                        <Form.Field 
                            control={Select}
                            name='destination' 
                            label='Destino del Credito' 
                            options={destinations} 
                            placeholder='Destino del Credito'
                            onChange={this.handleChange}
                            required
                            error={errors.destination}
                            loading={_loadSelect}
                        />                        
                        {
                            destination === 'Renovación de controladores fiscales' ? (
                                <Form.TextArea
                                    label='Vendedor del Controlador Fiscal'
                                    placeholder='Por favor indicanos a quién le vas a comprar el controlador fiscal.'
                                    name='vendedor'
                                    onChange={this.handleChange}
                                    required
                                    error={errors.vendedor}
                                />      
                            ) : null
                        }
                        <Form.Field>
                            <Checkbox 
                                label={<label>Acepto <a href='https://www.credility.com/terminosycondiciones' target="_blank"  rel='noopener noreferrer'>Términos y Condiciones</a></label>}
                                onChange={this.toggle}  
                                checked={this.state.checked} 
                            />
                        </Form.Field>
                        
                        <Button type='submit' style={{color: '#fff', background: '#EE3A43'}}>Continuar</Button>
                        <p>
                            Ya estás registrado? <a href="/login" >Logueate</a>
                        </p>
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
        message: state.step1Reducer.message,
        destinations: state.step1Reducer.destinos,
        redirect: state.loginReducer.stepRedirect,
        isLoggerdIn: state.loginReducer.isLoggerdIn
})

const mapDispatchToProps = (dispatch) => ({
    handleSendMail: (payload) => dispatch(sendAction(payload)),
    handleEmail: (email) => dispatch(addMailAction(email)),
    handleDestination: () => dispatch(getDestination())
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step1))

