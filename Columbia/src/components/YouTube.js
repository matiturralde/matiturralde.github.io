import React, { Component } from 'react'

export default class Youtube extends Component {
    render() {
        const {
            video,
            autoplay,
            rel,
            modest
        } = this.props

        const videoSrc = `https://www.youtube.com/embed/${video}?autoplay=${autoplay}&rel=${rel}&modestbranding=${modest}`

        return (
            <div>
                <iframe title='Instructivo' className="player" type="text/html" width="100%" height="280" src={videoSrc} frameBorder="0" />
            </div>
        )
    }
}
