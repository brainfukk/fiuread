import { Text } from 'react-native';
import styled from 'styled-components/native';


const PlainTextView = () => {
    return (
        <Container>
            <Group></Group>
        </Container>
    )
}

const Container = styled.View`
    flex: 1;
    margin-top: 50;
`;

export default PlainTextView;