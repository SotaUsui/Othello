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
        // this.socket = io.connect("http://localhost:3000");
        const serverIP = window.location.hostname;  // get the server IP dynamically
        this.socket = io.connect(`http://${serverIP}:3000`);


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

    handleCellClick(row, cell){
        // make sure if the game is not done
        if (this.state.isDone) {
            alert("Game over!");
            return;
        }

        // check the player turn
        if (this.state.currPlayer !== (this.props.player === "Player1" ? "B" : "W")) {
            alert("It's not your turn!");
            return;
        }

        // send the move of the player
        this.socket.emit("player_move", {
            room_id: this.props.roomId,
            place: [row, cell],
            turn: this.state.currPlayer
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

                <table id="board" style={{ borderCollapse: "collapse", margin: "auto" }}>
                    <tbody>
                        {this.state.board.map ((row, rowIndex) => (        // row index represent current row
                        <tr key={rowIndex}>
                            {row.map((cell, cellIndex) => (
                                <td
                                    key={cellIndex}
                                    onClick={
                                        pColor === this.state.currPlayer ?
                                        () => this.handleCellClick(rowIndex, cellIndex) : undefined
                                    }
                                    style={{
                                        width: "40px",
                                        height: "40px",
                                        border: "1px solid black",
                                        textAlign: "center",
                                        backgroundColor: "green",
                                        verticalAlign: "middle",

                                    }}
                                >
                                    {cell === 'W' && (
                                        <div
                                            style={{
                                                width: "30px",
                                                height: "30px",
                                                backgroundColor: "white",
                                                borderRadius: "50%",
                                                margin: "auto",
                                            }}
                                        />
                                    )}
                                    {cell === "B" && (
                                        <div
                                            style={{
                                                width: "30px",
                                                height: "30px",
                                                backgroundColor: "black",
                                                borderRadius: "50%",
                                                margin: "auto",
                                            }}
                                        />
                                    )}
                                </td>
                            ))}
                        </tr>
                    ))}

                    </tbody>
                </table>

            </div>
        );
    }
}

// Render the component with props from the HTML template
ReactDOM.render(
    <PvpGame roomId={roomId} player={player} />,
    document.getElementById("root")
);
