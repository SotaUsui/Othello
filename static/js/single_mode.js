
class SingleMode extends React.Component{

    constructor(props) {
        super(props);
        this.state = {
            board : props.data.board,
            curr_player : props.data.curr_player,
            message : props.data.message,
            valid : props.data.valid
        };
    }

    // draw the game board
    render() {
        const { board, curr_player, message, valid } = this.state;
        let player;
        if (curr_player === 'B'){
            player = "Black";
        }
        else{
            player = "White";
        }

        console.log(board);
        return (
            <div>
                <div id="turn"> {player} turn</div>

            <table id="board" style={{ borderCollapse: "collapse", margin: "auto" }}>
                <tbody>
                    {board.map ((row, rowIndex) => (        // row index represent current row
                        <tr key={rowIndex}>
                            {row.map((cell, cellIndex) => (
                                // each cell
                                <td
                                    key={cellIndex}
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
