class PvpGame extends React.Component {
    render() {
        // Determine the player's color based on the player name
        let pColor = (this.props.player === "Player1") ? "B" : "W";

        return (
            <div>
                <h1>Room ID: {this.props.roomId}</h1>
                <h2>You are {this.props.player}: {pColor}(color)</h2>
            </div>
        );
    }
}

// Render the component with props from the HTML template
ReactDOM.render(
    <PvpGame roomId={roomId} player={player} />,
    document.getElementById("root")
);
