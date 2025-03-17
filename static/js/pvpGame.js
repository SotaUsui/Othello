class PvpGame extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            board: [],
            currPlayer: "",
            score: (0,0),
            isDone: false
        };
        this.socket = null;
    }

    componentDidMount(){
        //this.socket = io.connect(`/game/${this.props.roomId}/${this.props.player}`);
        this.socket = io.connect("http://localhost:3000");

        // send game room id to the server
        this.socket.emit("game_state", {room_id: this.props.roomId});

        // receive the game infos (board, currPlayer, score, isDone)
        this.socket.on("game_update", (data) => {
            this.setState({
                board : data.board,
                currPlayer : data.currPlayer,
                score : data.score,
                isDone : data.isDone
            });
        });
    }



    render() {
        // Determine the player's color based on the player name
        let pColor = (this.props.player === "Player1") ? "B" : "W";
        let cPlayer = (this.state.currPlayer === 'B') ? "Player1" : "Player2"

        return (
            <div>
                <h1>Room ID: {this.props.roomId}</h1>
                <h2>You are {this.props.player}: {pColor}(color)</h2>
                <h3>Current Turn: {cPlayer}</h3>
                <h3>Score: {this.state.score[0]} - {this.state.score[1]}</h3>
                <h3>{this.state.board}</h3>
            </div>
        );
    }
}

// Render the component with props from the HTML template
ReactDOM.render(
    <PvpGame roomId={roomId} player={player} />,
    document.getElementById("root")
);
