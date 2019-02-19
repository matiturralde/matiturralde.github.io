import React, { Component } from 'react'
import { withRouter, Redirect } from 'react-router-dom'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Form, Grid } from 'semantic-ui-react'
import { validationAction } from './accions'

export class Callback extends Component {
    state = {
        _loading: true,
        _redirectTo: false,
        stepPath: '',
    }
    
    static propTypes = {
        
    }

    componentWillMount() {
        this.props.handleValidate({
            solicitudId: this.props.match.params.solicitudId
        }) 
    }

    componentWillReceiveProps(nextProps) {
        const {
            redirect
        } = nextProps;

        this.setState({
            stepPath: redirect,
            _redirectTo: true,
        })
        

    }

    render() {
        const {
            _loading,
            _redirectTo,
            stepPath
        } = this.state

        if (_redirectTo) {
            if (stepPath === 'step99') {
                return <Redirect to={{pathname: '/greeting'}} />
            } else {
                return <Redirect to={{pathname: stepPath}} />
            }            
        }
        
        const textHead = 'Procesando, aguarde unos instantes.'
        
        return (
            <Grid centered>
                <Grid.Column width={10}>
                    <h2 style={{color: '#EE3A43'}}>
                        {textHead}
                    </h2>
                    < br / >
                    < br / >
                    <Form loading={_loading}></Form>
                </Grid.Column>
            </Grid>
        )
    }
}

const mapStateToProps = (state) => ({
    redirect: state.callbackReducer.stepRedirect,
    isLoggerdIn: state.callbackReducer.isLoggerdIn
})

const mapDispatchToProps = (dispatch) => ({
    handleValidate: (payload) => dispatch(validationAction(payload))
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Callback))
