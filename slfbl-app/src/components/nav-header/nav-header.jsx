import { Link } from 'react-router-dom';
import './nav-header.css';

const NavHeader = () => {
    return (
        <header>
            <h1>Fantasy Baseball League</h1>
            <nav>
                <ul>
                    <li><Link to="/">Default</Link></li>
                    <li><Link to="/points">Points</Link></li>
                    <li><Link to="/matchup">Matchup</Link></li>
                </ul>
            </nav>
        </header>
    );
};

export default NavHeader;