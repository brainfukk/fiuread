import { Text } from 'react-native';
import { styled } from 'styled-components/native';


const PlainTextView = () => {
    return (
        <Container>
            <Text>Data</Text>
        </Container>
    )
}

const Container = styled.View`
    margin: 0 auto;
`;

export default PlainTextView;