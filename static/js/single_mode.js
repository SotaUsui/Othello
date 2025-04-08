
class SingleMode extends React.Component{

    constructor(props) {
        super(props);
        this.state = {
            board : props.data.board,
            curr_player : props.data.curr_player,
            message : props.data.message,
            valid : props.data.valid,
            game_over : false,
            winner :'',
            black : 2,
            white : 2,
        };
    }

    // get user input (row, col) and send to the server
    handleCellClick = async (row, col) => {
        try {
            const response = await fetch("/single-mode/move/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({row, col}),
            });

            const result = await response.json();

            // get the data back from server
            this.setState({
                board: result.board,
                curr_player: result.curr_player,
                message: result.message,
                valid : result.valid,
                game_over: result.game_over,
                black: result.black,
                white: result.white
            });
            if (this.state.game_over){
                this.game_result();
            }

        } catch (error) {
            console.error("Error:", error);
        }

    };


    AI_turn = async () => {
       try {
            const response = await fetch("/single-mode/ai/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ board: this.state.board }),
            });

            const result = await response.json();

            // get the data back from server
            this.setState({
                board: result.board,
                curr_player: result.curr_player,
                message: result.message,
                valid : result.valid,
                game_over : result.game_over,
                black : result.black,
                white : result.white
            });
            if (this.state.game_over){
                this.game_result();
            }

       } catch (error) {
            console.error("Error:", error);
       }

    };

    game_result = async () => {
       try {
            const response = await fetch("/single-mode/result/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ board: this.state.board }),
            });

            const result = await response.json();
            // Render the game result
            this.setState({ winner : result.winner,
                            black : result.black,
                            white : result.white
            });

       } catch (error) {
            console.error("Error:", error);
       }

    };

    goBackToMainMenu = () => {
        window.location.href = "/"; // Or use your routing method here
    };

    // draw the game board
    render() {
        const { board, curr_player, message, valid, game_over, winner, black, white } = this.state;

        let player;
        if (curr_player === 'B'){
            player = "Black";
        }
        else{
            player = "White";
            this.AI_turn();
        }

        return (
            <div>
                {!game_over && (
                    <>
                        <div id="turn"> <strong>{player}</strong> turn</div>
                        <div id="score"> Black {black} vs White {white}</div>
                    </>
                )}

                {game_over && (
                    <div className="result-modal">
                        <div className="modal-content">
                            <h2>Game End</h2>
                            <p>Winner: {winner}</p>
                            <p>Score: Black <strong>{black}</strong> vs White <strong>{white}</strong></p>
                            <button onClick={this.goBackToMainMenu}>Go to Main Menu</button>
                        </div>
                    </div>
                )}

            <table id="board" style={{ borderCollapse: "collapse", margin: "auto" }}>
                <tbody>
                    {board.map ((row, rowIndex) => (        // row index represent current row
                        <tr key={rowIndex}>
                            {row.map((cell, cellIndex) => (
                                // each cell
                                <td
                                    key={cellIndex}
                                    onClick={
                                        player === "Black" ?
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
ReactDOM.render(<SingleMode data={jsonfile} />, document.getElementById("root"));
