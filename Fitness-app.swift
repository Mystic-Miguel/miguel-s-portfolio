import SwiftUI

struct ContentView: View {
    @State private var displayValue = ""
    @State private var history = ""
    @State private var firstOperand = 0.0
    @State private var secondOperand = 0.0
    @State private var operation = ""
    
    let operationArray = ["×", "÷", "+", "-"]
    
    var body: some View {
        VStack(spacing: 20) {
            Spacer()
            Text(history)
                .font(.title)
                .foregroundColor(.white)
            
            Text(displayValue)
                .font(.largeTitle)
                .fontWeight(.bold)
                .lineLimit(1)
                .minimumScaleFactor(0.5)
                .foregroundColor(.white)
                .padding(.horizontal, 20)
                .frame(maxWidth: .infinity, alignment: .trailing)
            
            VStack(spacing: 10) {
                ForEach(0..<3) { row in
                    HStack(spacing: 10) {
                        ForEach(1..<4) { column in
                            NumberButton(number: row * 3 + column, action: {
                                displayValue += "\(row * 3 + column)"
                            })
                        }
                    }
                }
                
                HStack(spacing: 10) {
                    NumberButton(number: 0, action: {
                        if !displayValue.isEmpty {
                            displayValue += "0"
                        }
                    })
                    
                    NumberButton(number: -1, symbol: ".", action: {
                        if !displayValue.contains(".") {
                            displayValue += "."
                        }
                    })
                    
                    NumberButton(symbol: "=", color: .orange, action: {
                        if let operand = Double(displayValue) {
                            secondOperand = operand
                            let result = performOperation(firstOperand: firstOperand, secondOperand: secondOperand, operation: operation)
                            history = "\(firstOperand) \(operation) \(secondOperand) = \(result)"
                            displayValue = "\(result)"
                        }
                    })
                }
                
                HStack(spacing: 10) {
                    NumberButton(symbol: "C", color: .red, action: {
                        displayValue = ""
                        firstOperand = 0.0
                        secondOperand = 0.0
                        operation = ""
                        history = ""
                    })
                    
                    ForEach(operationArray, id: \.self) { op in
                        NumberButton(symbol: op, action: {
                            if let operand = Double(displayValue) {
                                firstOperand = operand
                                operation = op
                                history = "\(firstOperand) \(operation)"
                                displayValue = ""
                            }
                        })
                    }
                }
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 20)
        }
        .background(Color.black.edgesIgnoringSafeArea(.all))
    }
    
    func performOperation(firstOperand: Double, secondOperand: Double, operation: String) -> Double {
        switch operation {
        case "×":
            return firstOperand * secondOperand
        case "÷":
            return firstOperand / secondOperand
        case "+":
            return firstOperand + secondOperand
        case "-":
            return firstOperand - secondOperand
        default:
            return 0
        }
    }
}

struct NumberButton: View {
    var number: Int
    var symbol: String = ""
    var color: Color = .yellow
    var action: () -> Void
    
    var body: some View {
        Button(action: action) {
            if number >= 0 {
                Text("\(number)")
            } else {
                Text(symbol)
            }
        }
        .buttonStyle(NumberButtonStyle(color: color))
    }
}

struct NumberButtonStyle: ButtonStyle {
    var color: Color
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(width: 60, height: 60)
            .background(color)
            .foregroundColor(.white)
            .font(.title)
            .cornerRadius(30)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
